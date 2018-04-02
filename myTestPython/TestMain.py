import tensorflow as tf

flags = tf.app.flags
flags.DEFINE_boolean("myTest",       False,      "Test Tensorflow")
FLAGS = tf.app.flags.FLAGS
def test():
	print(FLAGS.myTest)
	print('This is Test')
print(__name__)
print(tf.app.flags)
if __name__ == '__main__':
	test()
