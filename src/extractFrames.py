import glob
import os
import shutil
import cv2


class Extractor(object):
    def __init__(self):
        pass

    def extract_labels(self, dataset):
        '''
        write all labels into labels.txt
        :param dataset directory etc: 'dataset/hmdb51_org'
        :return:
        '''
        classes_dir= glob.glob(dataset+ '/*')
        if os.path.exists('labels.txt'):
            os.remove('labels.txt')
        file = open('labels.txt', 'w')
        lb= lambda label: label.split(dataset)
        for class_dir in classes_dir:
            label= lb(class_dir)[1]
            # print(label)
            # labels.append(label)
            file.write(label+ '\n')
        file.close()

    def get_labels(self, dataset):
        '''
        get labels from .txt file
        :param dataset:
        :return:
        '''
        labels= []
        file = open('labels.txt', 'r')
        lines= file.readlines()
        for line in lines:
            labels.append(line.split('\n')[0])
        # print(labels)
        return labels

    def extraxt_frames(self, path_in, label, video_name):
        path_out= 'frames/'+ label+'/'+ video_name+ '/'
        if os.path.exists(path_out):
            shutil.rmtree(path_out)
        os.makedirs(path_out)
        cap= cv2.VideoCapture(path_in)
        count= 0
        video_names_txt= open(path_out+'video_names_txt.txt', 'w+')
        while cap.isOpened():
            ret, frame= cap.read()
            if ret is True:
                cv2.imwrite(os.path.join(path_out, 'frame{}.jpg'.format(count)), frame)
                print('extracting video {} on frame {}'.format(path_in, str(count)))
                # print(path_out+'frame{}.jpg'.format(str(count)))
                video_names_txt.writelines(path_out+'frame{}.jpg'.format(count) +'\n')
                count+= 1
            else:
                break
        video_names_txt.close()
        cap.release()
        cv2.destroyAllWindows()


extractor= Extractor()
# extractor.extract_labels('dataset/hmdb51_org/')
labels= extractor.get_labels('dataset/hmdb51_org/')
for label in labels:
    # file_names= [f.split('.avi')[0] for f in os.listdir('dataset/hmdb51_org/'+ label) if os.path.isfile(os.path.join('dataset/hmdb51_org/'+ label, f))]
    video_names= [f for f in os.listdir('dataset/hmdb51_org/'+ label) if os.path.isfile(os.path.join('dataset/hmdb51_org/'+ label, f))]
    # print(file_names)
    for video_name in video_names:
        # extractor.extraxt_frames('dataset/hmdb51_org/'+ label+'/'+ file_name)
        full_path= 'dataset/hmdb51_org/'+ label+'/'+ video_name
        print(full_path)
        # name= full_path.split('dataset/hmdb51_org/'+ label+'/').split('.avi')
        # print(video_name)
        # name= full_path.split('.avi')[0].split('dataset/hmdb51_org/'+label+'/')[1]
        name= full_path.strip('.avi').strip('dataset/hmdb51_org/'+label+'/')
        extractor.extraxt_frames(full_path, label, name)
        print(label)
        print(name)
        # break
    # break
# dataset/hmdb51_org/label/video_name
# extractor.extraxt_frames('dataset/hmdb51_org/climb/Kletter-WM_2005-_Speed_Achtelfinale_Herren_Minatchev_Hroza_climb_f_cm_np2_ba_med_2.avi', 'climb', 'Kletter-WM_2005-_Speed_Achtelfinale_Herren_Minatchev_Hroza_climb_f_cm_np2_ba_med_2')

#can improve performance by applying multithreading