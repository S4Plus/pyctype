"""Helper functions for DELF."""

from PIL import Image
import tensorflow as tf


def RgbLoader(path):
  """Helper function to read image with PIL.
  Args:
    path: Path to image to be loaded.
  Returns:
    PIL image in RGB format.
  """
  with tf.io.gfile.GFile(path, 'rb') as f:
    img = Image.open(f)
    return img.convert('RGB')

input_image_filename = ''
pil_im = RgbLoader(input_image_filename)
