from .filter import Filter
import sys
sys.path.append('../')
from utils.box import Box
import cv2
import numpy as np
import os

class T(Filter):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def get_name():
        return 't'
    
    @staticmethod
    def apply(box: Box, output_file: str = None):
        out = Filter.create_video_writer(output_file, box.fps, box.window)
        frames = box.frames
        for i in range(frames):
            k = int(i / frames * box.shape[3])
            im = cv2.resize(box[:, :, :, k], box.window)
            out.write(im)
        out.release()