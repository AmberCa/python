import tensorflow as tf

names_to_vars = {v.op.name: v for v in tf.global_variables()}
print(names_to_vars)

