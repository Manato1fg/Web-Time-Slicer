from .filter import Filter
import sys
sys.path.append('../')
from utils.box import Box
import cv2
import numpy as np
import os

class Y(Filter):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def get_name():
        return 'y'
    
    @staticmethod
    def apply(box: Box, output_file: str = None):
        out = Filter.create_video_writer(output_file, box.fps, box.window)
        frames = box.frames
        for i in range(frames):
            k = int(i / frames * box.shape[0])
            im = box[k, :, :, :]
            im = cv2.resize(im, box.window)
            out.write(im)
        out.release()