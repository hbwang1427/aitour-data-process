"""
inference with the MobileNet V2 model
"""
import os
import sys
import argparse
import pandas as pd
import json
import cv2
import numpy as np
import time
import tensorflow as tf
from array import array
import os
import struct

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
# The GPU id to use, usually either "0" or "1"
os.environ["CUDA_VISIBLE_DEVICES"]="" 

# First, pass the path of the image
image_size=224
num_channels=3
def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

def predict(image,graph):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    ##   Resizing the image to our desired size and preprocessing will be done exactly as done during training
    image = cv2.resize(image, (image_size, image_size), cv2.INTER_LINEAR)
    images = []
    images.append(image)
    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    #images = np.multiply(images, 1.0/255.0) #should not be used for this model!!!
    ##   The input to the network is of shape [None image_size image_size num_channels]. 
    ## Hence we reshape.
    x_batch = images.reshape(1, image_size,image_size,num_channels)

    ## NOW the complete graph with values has been restored
    y_pred = graph.get_tensor_by_name("head/out_emb:0")
    ## Let's feed the images to the input placeholders
    x= graph.get_tensor_by_name("input:0")
    y_test_images = np.zeros((1, 2))
    sess= tf.Session(graph=graph)
    ### Creating the feed_dict that is required to be fed to calculate y_pred 
    feed_dict_testing = {x: x_batch}
    
    return sess.run(y_pred, feed_dict=feed_dict_testing)   

def id2string(id_str):
    while(len(id_str))<6:
      id_str = '0'+id_str
    return id_str

def main(ar):
    #frozen_graph="../dl_models/museum/museum_256/museum_mobilenetv1_256.pb"
    #frozen_graph="../dl_models/museum/museum_512/museum_mobilenetv1_512.pb"
    frozen_graph="../dl_models/porcelain/porcelain_mark_256/porcelain_mark_256.pb"
    with tf.gfile.GFile(frozen_graph, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    with tf.Graph().as_default() as graph:
          tf.import_graph_def(graph_def,
                              input_map=None,
                              return_elements=None,
                              name=""
          )
    
    fpath = 'Images/boston'
    files = [f for f in os.listdir(fpath) if os.path.isfile(os.path.join(fpath,f))]        
    for f in files:
        if f.lower().endswith(('.png', '.jpg', '.jpeg', 'bmp')):
            if f.find('small')==-1:
                imname = os.path.join(fpath,f)
                img = cv2.imread(imname)
                if img is not None:
                    #with open('MET/visual_features/mobilenet_index_512.csv', 'ab') as fi:
                    #    fi.write("%s" % imname)
                    #    print(imname)
                    print(imname)
                    feature = predict(img,graph)
                    print(feature.flatten()) 
           
if __name__ == '__main__':
    main(sys.argv)
   #test_features()