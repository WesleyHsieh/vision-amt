from options import AMTOptions
import random
import tensorflow as tf
import cv2
from Net.tensor import inputdata, net3,net4,net6
import IPython
import numpy as np
import numpy.linalg as LA


class NetTest(object):

    def __init__(self,net_path):
        self.tf_net = net6.NetSix()
        self.tf_net_path = net_path
        self.sess = self.tf_net.load(var_path=self.tf_net_path)
        self.vals = []

    def computerER(self):
        sm = 0.0
        for val in self.vals:
            sm += val
        print "AVERAGE SQUARED EUCLIDEAN LOSS ",sm/len(self.vals)#*0.25

    def scale(self,deltas):
        deltas[0] = float(deltas[0])/0.2
        deltas[1] = float(deltas[1])/0.01
        deltas[2] = float(deltas[2])/0.005
        deltas[3] = float(deltas[3])/0.2
        return deltas
        
    def rollCall(self):
        train_path = AMTOptions.train_file
        test_path = AMTOptions.test_file
        deltas_path = AMTOptions.deltas_file

        print "Moving deltas from " + deltas_path + " to train: " + train_path + " and test: " + test_path

        deltas_file = open(deltas_path, 'r')

        for line in deltas_file:            
            path = AMTOptions.colors_dir
            labels = line.split()
            img_name = path+labels[0]
            deltas_t = labels[1:5]
            img = cv2.imread(img_name,1)
            img = np.reshape(img, (250, 250, 3))
            net_v = np.array(self.getNetOutput(img),dtype=np.float32)
            true_v = np.array(self.scale(deltas_t),dtype=np.float32)
            print "NET ",net_v
            print "TRYE ",true_v

            err = 0.5*LA.norm(net_v[0]-true_v[0])**2
            self.vals.append(err)

        self.computerER()


            

    def getNetOutput(self,img):
        return self.tf_net.output(self.sess, img,channels=3)


if __name__ == '__main__':

    nt = NetTest(net_path ='/media/1tb/Izzy/nets/net6_02-26-2016_18h08m10s.ckpt')
    nt.rollCall()

