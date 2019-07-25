import cv2 as cv
import numpy as np
# import glob
import numpy as np


class FaceDetection(object):
    def __init__(
        self, caffeModelTopoDir= 'models/face/pose_deploy.prototxt', caffeModelWeightDir= 'models/face/pose_iter_116000.caffemodel'
    ):
        self.caffeModelTopoDir= caffeModelTopoDir
        self.caffeModelWeightDir= caffeModelWeightDir

    def loadModel(self):
        return cv.dnn.readNetFromCaffe(self.caffeModelTopoDir, self.caffeModelWeightDir)

    def detector(self, frame ,net , threshold, npoints):
        frame= cv.imread(frame)
        frameCopy= np.copy(frame)
        shape= frame.shape
        width= shape[1]
        height= shape[0]
        aspectRatio= width/height
        inHeight= 368
        inWeight=int(((aspectRatio*inHeight)*8)//8)
        inBlob= cv.dnn.blobFromImage(frame, 1.0/255, (inWeight, inHeight), (0, 0, 0), swapRB= False, crop= False)
        # net= self.loadModel()
        net.setInput(inBlob)
        output= net.forward()
        # points= []
        # for i in range(npoints):
        #     proMap= output[0, i, :, :]
        #     print(proMap)
        #     proMap= cv.resize(proMap, (width, height))
        #     minVal, prob, minLoc, point= cv.minMaxLoc(proMap)
        #     if prob> threshold:
        #         cv.circle(frameCopy, (int(point[0]), int(point[1])), 3, (0, 255, 255), thickness=2, lineType=cv.FILLED)
        #         points.append(point)
        #     else:
        #         points.append(None)
        # # cv.imshow('',frameCopy)
        return output

        # print(output)


# faceDetector= FaceDetection()
# frameDir= 'dataset/frames/girl_smoking_a_cigarette_smoke_h_nm_np1_fr_med_2/frame113.jpg'
# net= faceDetector.loadModel()
# out= faceDetector.detector(frame= frameDir,net= net , threshold= 0.3, npoints= 67)
# print(out.shape)
# cv.waitKey(0)
# cv.destroyAllWindows()