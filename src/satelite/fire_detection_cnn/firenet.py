################################################################################

# Example : perform live fire detection in video using FireNet CNN

# Copyright (c) 2017/18 - Andrew Dunnings / Toby Breckon, Durham University, UK

# License : https://github.com/tobybreckon/fire-detection-cnn/blob/master/LICENSE

################################################################################

import cv2
import os
import sys
import math

################################################################################

import tflearn
from tflearn.layers.core import *
from tflearn.layers.conv import *
from tflearn.layers.normalization import *
from tflearn.layers.estimator import regression

################################################################################

def construct_firenet (x,y, training=False):

    # Build network as per architecture in [Dunnings/Breckon, 2018]

    network = tflearn.input_data(shape=[None, y, x, 3], dtype=tf.float32)

    network = conv_2d(network, 64, 5, strides=4, activation='relu')

    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)

    network = conv_2d(network, 128, 4, activation='relu')

    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)

    network = conv_2d(network, 256, 1, activation='relu')

    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)

    network = fully_connected(network, 4096, activation='tanh')
    if(training):
        network = dropout(network, 0.5)

    network = fully_connected(network, 4096, activation='tanh')
    if(training):
        network = dropout(network, 0.5)

    network = fully_connected(network, 2, activation='softmax')

    # if training then add training hyperparameters

    if(training):
        network = regression(network, optimizer='momentum',
                            loss='categorical_crossentropy',
                            learning_rate=0.001)

    # constuct final model

    model = tflearn.DNN(network, checkpoint_path='firenet',
                        max_checkpoints=1, tensorboard_verbose=2)

    return model

# construct and display model

model = construct_firenet(224, 224, training=False)

model.load(os.path.join("models/FireNet", "firenet"), weights_only=True)

def detect_fire(frame):
    small_frame = cv2.resize(frame, (rows, cols), cv2.INTER_AREA)

    output = model.predict([small_frame])

    if round(output[0][0]) == 1:
        return True
    else:
        return False

################################################################################

if __name__ == '__main__':
    # network input sizes

    rows = 224
    cols = 224

    if len(sys.argv) == 2:

        # load video file from first command line argument

        frame = cv2.imread(sys.argv[1])

        print(detect_fire(frame))

    else:
        print("usage: python firenet.py image.ext")

################################################################################
