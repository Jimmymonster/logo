This repo use opencv-python

Frame2Video
- input: Folder path that contain all frames, FPS, output path
- output : video

Video2Frame
- input: video file path, FPS, output frame folder path
- output: folder that contain frame

label crop
crop picture label based on yolo format (class mid_x mid_y width height)
the input folder structure should be like this

data
|--> images
|   |--> picture1.jpg
|   |--> picture2.jpg
|--> labels
    |--> picture1.txt
    |--> picture2.txt
