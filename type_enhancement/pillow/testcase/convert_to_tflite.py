"""Tools to convert a quantized deeplab model to tflite."""

import numpy as np
from PIL import Image
import tensorflow as tf


graph_def = ''
tflite_model = ''
image_path = ''
FLAGS = ''

"""Runs tflite and frozen graph on same input, check their outputs match."""
# Load tflite model and check input size.
interpreter = tf.lite.Interpreter(model_content=tflite_model)
var1 = interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height, width = input_details[0]['shape'][1:3]

# Prepare input image data.
with tf.io.gfile.GFile(image_path, 'rb') as f:
    image = Image.open(f)
var2 = image.convert('RGB')
var3 = var2.resize((width, height))
image = np.asarray(var3)
image = np.expand_dims(image, 0)

# Output from tflite model.
v4 = interpreter.set_tensor(input_details[0]['index'], image)
v5 = interpreter.invoke()
output_tflite = interpreter.get_tensor(output_details[0]['index'])

with tf.Graph().as_default():
    tf.graph_util.import_graph_def(graph_def, name='')
    with tf.compat.v1.Session() as sess:
      # Note here the graph will include preprocessing part of the graph
      # (e.g. resize, pad, normalize). Given the input image size is at the
      # crop size (backbone input size), resize / pad should be an identity op.
        output_graph = sess.run(
            FLAGS.output_tensor_name, feed_dict={'ImageTensor:0': image})

print('%.2f%% pixels have matched semantic labels.' % (
    100 * np.mean(output_graph == output_tflite)))
