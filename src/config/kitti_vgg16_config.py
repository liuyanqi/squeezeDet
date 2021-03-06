# Author: Bichen Wu (bichen@berkeley.edu) 08/25/2016

"""Model configuration for pascal dataset"""

import numpy as np

from config import base_model_config

def kitti_vgg16_config():
  """Specify the parameters to tune below."""
  mc                       = base_model_config('KITTI')

  mc.IMAGE_WIDTH           = 224
  mc.IMAGE_HEIGHT          = 224
  mc.BATCH_SIZE            = 20

  mc.WEIGHT_DECAY          = 0.0001
  mc.LEARNING_RATE         = 0.01
  mc.DECAY_STEPS           = 10000
  mc.MAX_GRAD_NORM         = 1.0
  mc.MOMENTUM              = 0.9
  mc.LR_DECAY_FACTOR       = 0.5

  mc.LOSS_COEF_BBOX        = 5.0
  mc.LOSS_COEF_CONF_POS    = 75.0
  mc.LOSS_COEF_CONF_NEG    = 100.0
  mc.LOSS_COEF_CLASS       = 1.0

  mc.PLOT_PROB_THRESH      = 0.4
  mc.NMS_THRESH            = 0.4
  mc.PROB_THRESH           = 0.005
  mc.TOP_N_DETECTION       = 64

  mc.DATA_AUGMENTATION     = True
  mc.DRIFT_X               = 150
  mc.DRIFT_Y               = 100
  mc.EXCLUDE_HARD_EXAMPLES = False

  mc.ANCHOR_SHAPE   = np.array(
                            [[100, 100]])

  mc.ANCHOR_BOX            = set_anchors(mc, 1)
  mc.ANCHOR_BOX2           = set_anchors(mc, 2)
  mc.ANCHOR_BOX3           = set_anchors(mc, 4)
  # print(mc.ANCHOR_BOX3)
  mc.ANCHORS               = len(mc.ANCHOR_BOX)
  mc.ANCHORS2              = len(mc.ANCHOR_BOX2)
  mc.ANCHORS3              = len(mc.ANCHOR_BOX3)
  # print(mc.ANCHORS, mc.ANCHORS2, mc.ANCHORS3)
  mc.ANCHOR_TOTAL          = mc.ANCHORS + mc.ANCHORS2 + mc.ANCHORS3

  mc.ANCHOR_PER_GRID       = 1

  # mc.ANCHOR_SHAPE          = np.array(
  #                               [[  36.,  37.], [ 366., 174.], [ 115.,  59.],
  #                                [ 162.,  87.], [  38.,  90.], [ 258., 173.],
  #                                [ 224., 108.], [  78., 170.], [  72.,  43.]])

  mc.PYRAMID_SCALE = [1, 2, 4]
  mc.SCALE_SIZE = 3
  mc.LOAD_PRETRAINED_MODEL = True
  return mc

def set_anchors(mc, s):
  H, W, B = 14*s, 14*s, 1

  print(H, W, B)
  print(mc.ANCHOR_SHAPE.shape)
  print(np.array([mc.ANCHOR_SHAPE]*H*W).shape)

  anchor_shapes = np.reshape(
      [mc.ANCHOR_SHAPE/s] * H * W,
      (H, W, B, 2)
  )
  center_x = np.reshape(
      np.transpose(
          np.reshape(
              np.array([np.arange(1, W+1)*float(mc.IMAGE_WIDTH)/(W+1)]*H*B), 
              (B, H, W)
          ),
          (1, 2, 0)
      ),
      (H, W, B, 1)
  )
  center_y = np.reshape(
      np.transpose(
          np.reshape(
              np.array([np.arange(1, H+1)*float(mc.IMAGE_HEIGHT)/(H+1)]*W*B),
              (B, W, H)
          ),
          (2, 1, 0)
      ),
      (H, W, B, 1)
  )
  anchors = np.reshape(
      np.concatenate((center_x, center_y, anchor_shapes), axis=3),
      (-1, 4)
  )
  print('anchors', anchors.shape)

  return anchors
