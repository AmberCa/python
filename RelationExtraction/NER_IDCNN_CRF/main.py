# encoding=utf8
import os
import sys
sys.path.append(os.getcwd()+ '/NER_IDCNN_CRF')
# print(sys.path)

import codecs
import pickle
import itertools
from collections import OrderedDict

import tensorflow as tf
import numpy as np
from model import Model
from loader import load_sentences, update_tag_scheme
from loader import char_mapping, tag_mapping
from loader import augment_with_pretrained, prepare_dataset
from utils import get_logger, make_path, clean, create_model, save_model
from utils import print_config, save_config, load_config, test_ner
from data_utils import load_word2vec, create_input, input_from_line, BatchManager
from nerControllerConfig import NerControllerConfig

flags = tf.app.flags
flags.DEFINE_boolean("clean",       False,      "clean train folder")
flags.DEFINE_boolean("train",       False,      "Whether train the model")
# configurations for the model
flags.DEFINE_integer("seg_dim",     20,         "Embedding size for segmentation, 0 if not used")
flags.DEFINE_integer("char_dim",    100,        "Embedding size for characters")
flags.DEFINE_integer("lstm_dim",    100,        "Num of hidden units in LSTM, or num of filters in IDCNN")
flags.DEFINE_string("tag_schema",   "iobes",    "tagging schema iobes or iob")

# configurations for training
flags.DEFINE_float("clip",          5,          "Gradient clip")
flags.DEFINE_float("dropout",       0.5,        "Dropout rate")
flags.DEFINE_float("batch_size",    20,         "batch size")
flags.DEFINE_float("lr",            0.001,      "Initial learning rate")
flags.DEFINE_string("optimizer",    "adam",     "Optimizer for training")
flags.DEFINE_boolean("pre_emb",     True,       "Wither use pre-trained embedding")
flags.DEFINE_boolean("zeros",       False,      "Wither replace digits with zero")
flags.DEFINE_boolean("lower",       True,       "Wither lower case")

flags.DEFINE_integer("max_epoch",   100,        "maximum training epochs")
flags.DEFINE_integer("steps_check", 100,        "steps per checkpoint")
flags.DEFINE_string("ckpt_path",    "ckpt_IDCNN",      "Path to save model")
flags.DEFINE_string("summary_path", "summary",      "Path to store summaries")
flags.DEFINE_string("log_file",     "train.log",    "File for log")
flags.DEFINE_string("map_file",     "maps.pkl",     "file for maps")
flags.DEFINE_string("vocab_file",   "vocab.json",   "File for vocab")
flags.DEFINE_string("config_file",  "config_file",  "File for config")
flags.DEFINE_string("script",       "conlleval",    "evaluation script")
flags.DEFINE_string("result_path",  "result",       "Path for results")
flags.DEFINE_string("emb_file",     os.path.join("data", "vec.txt"),  "Path for pre_trained embedding")
# flags.DEFINE_string("train_file",   os.path.join("data", "example.train"),  "Path for train data")
# flags.DEFINE_string("dev_file",     os.path.join("data", "example.dev"),    "Path for dev data")
# flags.DEFINE_string("test_file",    os.path.join("data", "example.test"),   "Path for test data")
flags.DEFINE_string("train_file",   "example.train",  "Path for train data")
flags.DEFINE_string("dev_file",     "example.dev",    "Path for dev data")
flags.DEFINE_string("test_file",    "example.test",   "Path for test data")
#add dbj
#train parameters
flags.DEFINE_string("modelSavePath", 'per',   "Path for save model")
# flags.DEFINE_string("trainPath", 'per',   "Path for train data")

flags.DEFINE_string("model_type", "idcnn", "Model type, can be idcnn or bilstm")
#flags.DEFINE_string("model_type", "bilstm", "Model type, can be idcnn or bilstm")

FLAGS = tf.app.flags.FLAGS
assert FLAGS.clip < 5.1, "gradient clip should't be too much"
assert 0 <= FLAGS.dropout < 1, "dropout rate between 0 and 1"
assert FLAGS.lr > 0, "learning rate must larger than zero"
assert FLAGS.optimizer in ["adam", "sgd", "adagrad"]

# config for the model
def config_model(char_to_id, tag_to_id):
    config = OrderedDict()
    config["model_type"] = FLAGS.model_type
    config["num_chars"] = len(char_to_id)
    config["char_dim"] = FLAGS.char_dim
    config["num_tags"] = len(tag_to_id)
    config["seg_dim"] = FLAGS.seg_dim
    config["lstm_dim"] = FLAGS.lstm_dim
    config["batch_size"] = FLAGS.batch_size

    config["emb_file"] = FLAGS.emb_file
    config["clip"] = FLAGS.clip
    config["dropout_keep"] = 1.0 - FLAGS.dropout
    config["optimizer"] = FLAGS.optimizer
    config["lr"] = FLAGS.lr
    config["tag_schema"] = FLAGS.tag_schema
    config["pre_emb"] = FLAGS.pre_emb
    config["zeros"] = FLAGS.zeros
    config["lower"] = FLAGS.lower
    return config


def evaluate(sess, model, name, data, id_to_tag, logger):
    logger.info("evaluate:{}".format(name))
    ner_results = model.evaluate(sess, data, id_to_tag)
    eval_lines = test_ner(ner_results, FLAGS.result_path)# + '/' + FLAGS.modelSavePath
    for line in eval_lines:
        logger.info(line)
    f1 = float(eval_lines[1].strip().split()[-1])

    if name == "dev":
        # model.best_dev_f1 = float(model.best_dev_f1)
        best_test_f1 = model.best_dev_f1.eval()
        if f1 > best_test_f1:
            tf.assign(model.best_dev_f1, f1).eval()
            logger.info("new best dev f1 score:{:>.3f}".format(f1))
        return f1 > best_test_f1
    elif name == "test":
        # model.best_test_f1 = float(model.best_test_f1)
        best_test_f1 = model.best_test_f1.eval()
        if f1 > best_test_f1:
            tf.assign(model.best_test_f1, f1).eval()
            logger.info("new best test f1 score:{:>.3f}".format(f1))
        return f1 > best_test_f1


def train():
    trainPath = 'data/' + FLAGS.modelSavePath + '/'
    mapFile = 'data/mapfiles/' + FLAGS.modelSavePath + '/'
    modelSavePath = '/' + FLAGS.modelSavePath
    configFile = 'configfiles/' + FLAGS.modelSavePath + '/'
    # load data sets
    train_sentences = load_sentences(trainPath + FLAGS.train_file, FLAGS.lower, FLAGS.zeros)
    dev_sentences = load_sentences(trainPath + FLAGS.dev_file, FLAGS.lower, FLAGS.zeros)
    test_sentences = load_sentences(trainPath + FLAGS.test_file, FLAGS.lower, FLAGS.zeros)

    # Use selected tagging scheme (IOB / IOBES)
    update_tag_scheme(train_sentences, FLAGS.tag_schema)
    update_tag_scheme(test_sentences, FLAGS.tag_schema)

    # create maps if not exist
    if not os.path.isfile(mapFile + FLAGS.map_file):
        # create dictionary for word
        if FLAGS.pre_emb:
            dico_chars_train = char_mapping(train_sentences, FLAGS.lower)[0]
            dico_chars, char_to_id, id_to_char = augment_with_pretrained(
                dico_chars_train.copy(),
                FLAGS.emb_file,
                list(itertools.chain.from_iterable(
                    [[w[0] for w in s] for s in test_sentences])
                )
            )
        else:
            _c, char_to_id, id_to_char = char_mapping(train_sentences, FLAGS.lower)

        # Create a dictionary and a mapping for tags
        _t, tag_to_id, id_to_tag = tag_mapping(train_sentences)
        with open(mapFile + FLAGS.map_file, "wb") as f:
            pickle.dump([char_to_id, id_to_char, tag_to_id, id_to_tag], f)
    else:
        with open(mapFile + FLAGS.map_file, "rb") as f:
            char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)

    # prepare data, get a collection of list containing index
    train_data = prepare_dataset(
        train_sentences, char_to_id, tag_to_id, FLAGS.lower
    )
    dev_data = prepare_dataset(
        dev_sentences, char_to_id, tag_to_id, FLAGS.lower
    )
    test_data = prepare_dataset(
        test_sentences, char_to_id, tag_to_id, FLAGS.lower
    )
    print("%i / %i / %i sentences in train / dev / test." % (
        len(train_data), len(dev_data), len(test_data)))

    train_manager = BatchManager(train_data, FLAGS.batch_size)
    dev_manager = BatchManager(dev_data, 100)
    test_manager = BatchManager(test_data, 100)
    # make path for store log and model if not exist
    make_path(FLAGS)
    if os.path.isfile(configFile + FLAGS.config_file):# 
        config = load_config(configFile + FLAGS.config_file)
    else:
        config = config_model(char_to_id, tag_to_id)
        save_config(config, configFile + FLAGS.config_file)
    make_path(FLAGS)
    print('configFile + FLAGS.config_file-----------------%s'%configFile + FLAGS.config_file)
    log_path = os.path.join("log", FLAGS.log_file)
    logger = get_logger(log_path)
    print_config(config, logger)

    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    steps_per_epoch = train_manager.len_data
    with tf.Session(config=tf_config) as sess:
        model = create_model(sess, Model, FLAGS.ckpt_path + modelSavePath, load_word2vec, config, id_to_char, logger, FLAGS.modelSavePath)
        logger.info("start training")
        loss = []
        for i in range(100):
            for batch in train_manager.iter_batch(shuffle=True):
                step, batch_loss = model.run_step(sess, True, batch)
                loss.append(batch_loss)
                if step % FLAGS.steps_check == 0:
                    iteration = step // steps_per_epoch + 1
                    logger.info("iteration:{} step:{}/{}, "
                                "NER loss:{:>9.6f}".format(
                        iteration, step%steps_per_epoch, steps_per_epoch, np.mean(loss)))
                    loss = []

            best = evaluate(sess, model, "dev", dev_manager, id_to_tag, logger)
            if best:
                save_model(sess, model, FLAGS.ckpt_path  + modelSavePath, logger)
            evaluate(sess, model, "test", test_manager, id_to_tag, logger)


def evaluate_line():
    configFile = 'configfiles/' + FLAGS.modelSavePath + '/'
    mapFile = 'data/mapfiles/' + FLAGS.modelSavePath + '/'
    config = load_config(configFile + FLAGS.config_file)#
    logger = get_logger(FLAGS.log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(mapFile + FLAGS.map_file, "rb") as f:
        char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        model = create_model(sess, Model, FLAGS.ckpt_path + '/' + FLAGS.modelSavePath, load_word2vec, config, id_to_char, logger, FLAGS.modelSavePath)
        while True:
            # try:
            #     line = input("请输入测试句子:")
            #     result = model.evaluate_line(sess, input_from_line(line, char_to_id), id_to_tag)
            #     print(result)
            # except Exception as e:
            #     logger.info(e)

                line = input("请输入测试句子:")
                result = model.evaluate_line(sess, input_from_line(line, char_to_id), id_to_tag)
                print(result)

def evaluate_line2(sentenceInfo):#sentenceInfo
    pathNew = os.getcwd() +'/NER_IDCNN_CRF/'
    config = load_config(pathNew + FLAGS.config_file)
    logger = get_logger(pathNew + FLAGS.log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(pathNew + mapFile + FLAGS.map_file, "rb") as f:
        char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        model = create_model(sess, Model, pathNew +  FLAGS.ckpt_path + '/'+ FLAGS.modelSavePath, load_word2vec, config, id_to_char, logger)
        # while True:
            # try:
            #     line = input("请输入测试句子:")
            #     result = model.evaluate_line(sess, input_from_line(line, char_to_id), id_to_tag)
            #     print(result)
            # except Exception as e:
            #     logger.info(e)

        # line = input("请输入测试句子:")
        result = model.evaluate_line(sess, input_from_line(sentenceInfo, char_to_id), id_to_tag)
        print(result)
        # del(model)
        return result

#*********************************
def getEntity(sentenceInfo):
    pathNew = os.getcwd() +'/NER_IDCNN_CRF/'
    configFile = pathNew + 'configfiles/' + FLAGS.modelSavePath + '/'
    mapFile = 'data/mapfiles/' + FLAGS.modelSavePath + '/'
   
    print('NerControllerConfig.NER_CONTROLLER_FLAG------%s'%NerControllerConfig.NER_CONTROLLER_FLAG)
    if not NerControllerConfig.NER_CONTROLLER_FLAG:
        config = load_config(configFile + FLAGS.config_file)
        logger = get_logger(pathNew + FLAGS.log_file)
        # limit GPU memory
        tf_config = tf.ConfigProto()
        tf_config.gpu_options.allow_growth = True
        NerControllerConfig.tf_config = tf_config
        with open(pathNew + mapFile + FLAGS.map_file, "rb") as f:
            NerControllerConfig.char_to_id, id_to_char, tag_to_id, NerControllerConfig.id_to_tag = pickle.load(f)
        with tf.Session(config=tf_config) as sess:
            # NerControllerConfig.sess = sess
            NerControllerConfig.NER_CONTROLLER_FLAG = True
            NerControllerConfig.entity_ckpy = tf.train.get_checkpoint_state(pathNew +  FLAGS.ckpt_path + '/'+ FLAGS.modelSavePath)
            NerControllerConfig.model = create_model(sess, Model, pathNew +  FLAGS.ckpt_path + '/'+ FLAGS.modelSavePath, load_word2vec, config, id_to_char, logger)
    print('-----------实体提取')
    with tf.Session(config=NerControllerConfig.tf_config) as sess2:
        NerControllerConfig.model.saver.restore(sess2, NerControllerConfig.entity_ckpy.model_checkpoint_path)
        result = NerControllerConfig.model.evaluate_line(sess2, input_from_line(sentenceInfo, NerControllerConfig.char_to_id), NerControllerConfig.id_to_tag)
        print(result)
        return result

def getEntity6(sentenceInfo, modelTpye):
    pathNew = os.getcwd() +'/NER_IDCNN_CRF/'
    configFile = pathNew + 'configfiles/' + modelTpye + '/'
    mapFile = 'data/mapfiles/' + modelTpye + '/'
   
    print('NerControllerConfig.NER_CONTROLLER_FLAG------%s'%NerControllerConfig.NER_CONTROLLER_FLAG[modelTpye])
    if not NerControllerConfig.NER_CONTROLLER_FLAG[modelTpye]:
        config = load_config(configFile + FLAGS.config_file)
        logger = get_logger(pathNew + FLAGS.log_file)
        # limit GPU memory
        tf_config = tf.ConfigProto()
        tf_config.gpu_options.allow_growth = True
        NerControllerConfig.tf_config[modelTpye] = tf_config
        with open(pathNew + mapFile + FLAGS.map_file, "rb") as f:
            NerControllerConfig.char_to_id[modelTpye], id_to_char, tag_to_id, NerControllerConfig.id_to_tag[modelTpye] = pickle.load(f)
        with tf.Session(config=tf_config) as sess:
            # NerControllerConfig.sess = sess
            NerControllerConfig.NER_CONTROLLER_FLAG[modelTpye] = True
            NerControllerConfig.entity_ckpy[modelTpye] = tf.train.get_checkpoint_state(pathNew +  FLAGS.ckpt_path + '/'+ modelTpye)
            NerControllerConfig.model[modelTpye] = create_model(sess, Model, pathNew +  FLAGS.ckpt_path + '/'+ modelTpye, load_word2vec, config, id_to_char, logger, modelTpye)
    print('-----------实体提取')
    with tf.Session(config=NerControllerConfig.tf_config[modelTpye]) as sess2:
        NerControllerConfig.model[modelTpye].saver.restore(sess2, NerControllerConfig.entity_ckpy[modelTpye].model_checkpoint_path)
        result = NerControllerConfig.model[modelTpye].evaluate_line(sess2, input_from_line(sentenceInfo, NerControllerConfig.char_to_id[modelTpye]), NerControllerConfig.id_to_tag[modelTpye])
        # print(result)
        return result


def getEntity2():#sentenceInfo
    pathNew = os.getcwd() +'/NER_IDCNN_CRF/'
    mapFile = 'data/mapfiles/' + FLAGS.modelSavePath + '/'
    config = load_config(pathNew + FLAGS.config_file)
    logger = get_logger(pathNew + FLAGS.log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    NerControllerConfig.tf_config = tf_config
    with open(pathNew + mapFile + FLAGS.map_file, "rb") as f:
        NerControllerConfig.char_to_id, id_to_char, tag_to_id, NerControllerConfig.id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        # NerControllerConfig.sess = sess
        if not NerControllerConfig.NER_CONTROLLER_FLAG:
            NerControllerConfig.NER_CONTROLLER_FLAG = True
            NerControllerConfig.entity_ckpy = tf.train.get_checkpoint_state(pathNew +  FLAGS.ckpt_path + '/'+ FLAGS.modelSavePath)
            NerControllerConfig.model = create_model(sess, Model, pathNew +  FLAGS.ckpt_path + '/'+ FLAGS.modelSavePath, load_word2vec, config, id_to_char, logger)
            # result =  NerControllerConfig.model.evaluate_line(sess, input_from_line(sentenceInfo,  NerControllerConfig.char_to_id),  NerControllerConfig.id_to_tag)
            # return result
        
        # ckpt = tf.train.get_checkpoint_state(pathNew +  FLAGS.ckpt_path + '/'+ FLAGS.modelSavePath)
        # NerControllerConfig.model.saver.restore(sess, NerControllerConfig.entity_ckpy.model_checkpoint_path)
        # result =  NerControllerConfig.model.evaluate_line(sess, input_from_line(sentenceInfo,  NerControllerConfig.char_to_id),  NerControllerConfig.id_to_tag)
        # return result


def main(_):

    if FLAGS.train:
        if FLAGS.clean:
            clean(FLAGS)
        train()
    else:
        evaluate_line()


if __name__ == "__main__":
    tf.app.run(main)



