@echo off
echo .
echo -------------------------------------------------
echo Este programa requiere los siguientes programas:
echo tensorflow = 1.15
echo opencv = 4.x

python TFLite_detection_video.py --modeldir=model --video=Multimedia/video2.mp4