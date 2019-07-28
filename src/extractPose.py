import cv2
import numpy as np
import os
import shutil

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

    def get_output_of_net(self, net, frame_dir, npoints, threshold):
        '''
        -   The output of pre-train model is a 4D matrix:
        -   The first dimension is image ID
        -   The second are score of points. MPI returns a set of 44 points. We just use some of them, depending on what we need
        -   The 3rd is height of output map
        -   The 4th is width of output map
        -   We use the threshold value for decreasing wrong detections
        :param net: caffemodel
        :param frame_dir: directory of frame
        :param npoints: number of points
        :param threshold: threshold
        :return: matrix of points probability
        '''
        frame= cv2.imread(frame_dir)
        # shape= frame.shape
        height, width, channels = frame.shape
        # print(shape)
        # width = shape[1]
        # height = shape[0]
        shape= (width, height)
        aspect_ratio = width / height
        input_height = 368
        input_weight = int(((aspect_ratio * input_height) * 8) // 8)
        input_blob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (input_weight, input_height), (0, 0, 0), swapRB=False, crop=False)
        # net= self.loadModel()
        net.setInput(input_blob)
        output = net.forward()
        points = []
        for i in range(npoints):
            pro_map = output[0, i, :, :]
            pro_map = cv2.resize(pro_map, shape)
            minVal, prob, minLoc, point = cv2.minMaxLoc(pro_map)
            if prob > threshold:
                # cv2.circle(image, (int(point[0]), int(point[1])), 3, (0, 255, 255), thickness=2, lineType=cv2.FILLED)
                points.append(point)
            else:
                points.append(None)
        if os.path.exists('pose25points.txt'):
            os.remove('pose25points.txt')
        file = open('pose25points.txt', 'w+')
        file.write(str(points))
        file.close()
        return output, shape, points

    def draw(self, output_of_net, img_dir, npoints, shape, threshold):
        '''
        -   The output of pre-train model is a 4D matrix:
        -   The first dimension is image ID
        -   The second are score of points. MPI returns a set of 44 points. We just use some of them, depending on what we need
        -   The 3rd is height of output map
        -   The 4th is width of output map
        -   We use the threshold value for decreasing wrong detections
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
        return points


prototxt= 'models/pose/body_25/pose_deploy.prototxt'
weight= 'models/pose/body_25/pose_iter_584000.caffemodel'
poses_extraction= Poses_extraction(prototxt= prototxt, weight= weight)
net= poses_extraction.load_model()

# img= 'frames/climb/Julius_Haushammer___Klettern_und_Bouldern___1979_climb_f_cm_np1_ba_med_0/frame0.jpg'
# output, shape, points= poses_extraction.get_output_of_net(net= net, frame_dir= img, npoints= 25, threshold= 0.1)
# print(output.shape[2])
# poses_extraction.draw(output_of_net= output, img_dir= img, npoints= 25, shape= shape, threshold= 0.1)

import glob
paths= glob.glob('frames/*')
print(paths)
for path in paths:
    sub_paths= glob.glob(path+'/*')
    # print(sub_paths)
    for sub_path in sub_paths:
        txt_files= glob.glob(sub_path+'/*.txt')
        for txt_file in txt_files:
            txt_file= open(txt_file, 'r')
            # print(txt_file.readlines())
            txt_lines= txt_file.readlines()
            print(txt_lines)
            if os.path.exists('poses'+ path.strip('frames')):
                shutil.rmtree('poses'+ path.strip('frames'))
            os.makedirs('poses'+ path.strip('frames'))
            poses_txt = open('poses' + sub_path.strip('frames') + '.txt', 'w+')
            for i in range(len(txt_lines)):
                if i%4== 0:
                    poses_txt = open('poses' + sub_path.strip('frames') + '.txt', 'a+')
                    frame_dir= txt_lines[i].strip('\n')
                    print(frame_dir)
                    print(i)
                    output, shape, points= poses_extraction.get_output_of_net(net= net, frame_dir= frame_dir, npoints= 25, threshold= 0.1)
                    # points= poses_extraction.draw(output_of_net= net, img_dir= txt_lines[i].strip('\n'), npoints= 25, threshold= 0.1)
                    print(points)
                    poses_txt.write(str(points)+'\n')
            poses_txt.close()
