import cv2
import numpy as np
import os

class Poses_extraction(object):
    def __init__(self, prototxt, weight):
        self.prototxt= prototxt
        self.weight= weight
        pass

    def load_model(self):
        '''
        :return: net
        '''
        return cv2.dnn.readNetFromCaffe(self.prototxt, self.weight)

    def get_output_of_net(self, net, frame_dir):
        '''
        :param net: caffemodel
        :param frame_dir: directory of frame
        :return: matrix of points probability
        '''
        frame= cv2.imread(frame_dir)
        shape= frame.shape
        width = shape[1]
        height = shape[0]
        shape= (width, height)
        aspect_ratio = width / height
        input_height = 368
        input_weight = int(((aspect_ratio * input_height) * 8) // 8)
        input_blob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (input_weight, input_height), (0, 0, 0), swapRB=False, crop=False)
        # net= self.loadModel()
        net.setInput(input_blob)
        output = net.forward()
        return output, shape

    def draw(self, output_of_net, img_dir, npoints, shape, threshold):
        '''
        :param output_of_net: output of caffemodel net
        :param img_dir: image dir
        :param npoints: number of pose points
        :param shape: (tuple)
        :return:
        '''
        image= cv2.imread(img_dir)
        points= []
        for i in range(npoints):
            pro_map= output_of_net[0, i, :, :]
            pro_map= cv2.resize(pro_map, shape)
            minVal, prob, minLoc, point = cv2.minMaxLoc(pro_map)
            if prob> threshold:
                cv2.circle(image, (int(point[0]), int(point[1])), 3, (0, 255, 255), thickness=2, lineType=cv2.FILLED)
                points.append(point)
            else:
                points.append(None)
        cv2.imshow('img', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


prototxt= 'models/pose/body_25/pose_deploy.prototxt'
weight= 'models/pose/body_25/pose_iter_584000.caffemodel'
poses_extraction= Poses_extraction(prototxt= prototxt, weight= weight)
net= poses_extraction.load_model()

img= 'resources/frame9.jpg'
output, shape= poses_extraction.get_output_of_net(net= net, frame_dir= img)
poses_extraction.draw(output_of_net= output, img_dir= img, npoints= 25, shape= shape, threshold= 0.1)

print(output)
if os.path.exists('pose25points.txt'):
    os.remove('pose25points.txt')
file= open('pose25points.txt', 'w+')
file.write(str(output))
file.close()
