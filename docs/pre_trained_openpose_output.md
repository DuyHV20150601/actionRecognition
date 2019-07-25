#   Openpose
##  1.  openpose points definition
### 1.1.    COCO model
![coco 15](/resources/coco15.png)

`Nose – 0, Neck – 1, Right Shoulder – 2, Right Elbow – 3, Right Wrist – 4,
Left Shoulder – 5, Left Elbow – 6, Left Wrist – 7, Right Hip – 8, Right Knee – 9, Right Ankle – 10, Left Hip – 11, Left Knee – 12, LAnkle – 13, Right Eye – 14, Left Eye – 15, Right Ear – 16, Left Ear – 17, Background – 18`
### 1.2.    MPI

`Head – 0, Neck – 1, Right Shoulder – 2, Right Elbow – 3, Right Wrist – 4, Left Shoulder – 5, Left Elbow – 6, Left Wrist – 7, Right Hip – 8, Right Knee – 9, Right Ankle – 10, Left Hip – 11, Left Knee – 12, Left Ankle – 13, Chest – 14, Background – 15`
### 1.3.    BODY_25
![BODY_25](/resources/pose25.png)
`{0,  "Nose"}, {1,  "Neck"}, {2,  "RShoulder"}, {3,  "RElbow"}, {4,  "RWrist"}, {5,  "LShoulder"}, {6,  "LElbow"}, {7,  "LWrist"}, {8,  "MidHip"}, {9,  "RHip"}, {10, "RKnee"}, {11, "RAnkle"}, {12, "LHip"}, {13, "LKnee"}, {14, "LAnkle"}, {15, "REye"}, {16, "LEye"}, {17, "REar"}, {18, "LEar"}, {19, "LBigToe"}, {20, "LSmallToe"}, {21, "LHeel"}, {22, "RBigToe"}, {23, "RSmallToe"}, {24, "RHeel"}, {25, "Background"}`

##  2.  openpose output format

-   The output of pre-train model is a 4D matrix:
    -   The first dimension is image ID
    -   The second are score of points. MPI returns a set of 44 points. We just use some of them, depending on what we need
    -   The 3rd is height of output map
    -   The 4th is width of output map
-   We use the threshold value for decreasing wrong detections