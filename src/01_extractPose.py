# From Python
# It requires OpenCV installed for Python
import sys
import cv2 as cv
import os
from sys import platform
import argparse
import time
import numpy as np

# Import Openpose (Windows/Ubuntu/OSX)
# dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path="/media/nhquan/PHD/openpose/build/"
try:
	# Windows Import
	if platform == "win32":
		# Change these variables to point to the correct folder (Release/x64 etc.) 
		sys.path.append(dir_path + 'python/openpose/Release');
		os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
		import pyopenpose as op
	else:
		# Change these variables to point to the correct folder (Release/x64 etc.) 
		sys.path.append(dir_path+'python');
		# If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
		# sys.path.append('/usr/local/python')
		from openpose import pyopenpose as op
except ImportError as e:
	print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
	raise e

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--video_dir", default="/media/nhquan/PHD/openpose/examples/media/COCO_val2014_000000000192.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "/media/nhquan/PHD/openpose/models/"

# Add others in path?
for i in range(0, len(args[1])):
	curr_item = args[1][i]
	if i != len(args[1])-1: next_item = args[1][i+1]
	else: next_item = "1"
	if "--" in curr_item and "--" in next_item:
		key = curr_item.replace('-','')
		if key not in params:  params[key] = "1"
	elif "--" in curr_item and "--" not in next_item:
		key = curr_item.replace('-','')
		if key not in params: params[key] = next_item

# # Construct it from system arguments
# # op.init_argv(args[1])
# # oppython = op.OpenposePython()

try:
	# Starting OpenPose
	opWrapper = op.WrapperPython()
	opWrapper.configure(params)
	opWrapper.start()

	# Process video
	video_Dir="./datasets/"
	feature_Dir="./poses/"

	for root, dirs, files in os.walk(video_Dir):    	
		if root==video_Dir:
			for d in dirs:
				sd=os.path.join(feature_Dir,d)				
				if not os.path.exists(sd):
					os.mkdir(sd)
					print("Directory " , sd ,  " Created ")
		else:
			print("%s_%d_%d" % (root,len(dirs),len(files)))
			for video in files:
				videoFile=os.path.join(root,video)				
				poseFile=videoFile.replace("datasets","poses")
				poseFile=poseFile.replace(".avi",".txt")
				print(videoFile)
				print(poseFile)
				vid_cap = cv.VideoCapture(videoFile)
				with open(poseFile, "a") as myfile:						
					success,frame = vid_cap.read()						
					frNo=0	
					datum = op.Datum()
					while success: 	
						start_time=time.time()
						print ('frame: %d ' % (frNo))
						#frameResize = cv.resize(frame,None,fx=0.8, fy=0.8, interpolation = cv.INTER_CUBIC)						
						datum.cvInputData = frame
						opWrapper.emplaceAndPop([datum])
						s=datum.poseKeypoints.size
						print(s)
						if s>18:
							myfile.write("%d " %(frNo))  	#np.savetxt(myfile,[frNo], delimiter=' ',fmt='%i');							
							shape=datum.poseKeypoints.shape														
							myfile.write("%d %d %d " %(shape[0],shape[1],shape[2])) 	#np.savetxt(myfile,[[shape[0],shape[1],shape[2]]], delimiter=' ',fmt='%i');
							poseData=datum.poseKeypoints.reshape(shape[0]*shape[1]*shape[2])							
							for i in range(s-1):
								myfile.write("%1.3f " %(poseData[i])) #np.savetxt(myfile,datum.poseKeypoints.reshape(1,shape[0]*shape[1]*shape[2]),delimiter=' ',fmt='%1.2f')							
							myfile.write("%1.3f\n" %(poseData[s-1])) 
						cv.imshow("OpenPose 1.4.0", datum.cvOutputData) 
						key=cv.waitKey(1)
						if key==27:
							break
						success,frame = vid_cap.read()	
						frNo +=1
						print('Took %.2f ms.' % (1000 * (time.time() - start_time)))
			# 	break
			# break
except Exception as e:
	print(e)
	pass #sys.exit(-1)
