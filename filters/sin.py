from .filter import Filter
import sys
sys.path.append('../')
from utils.box import Box
import cv2
import numpy as np
import os
import math

class Sin(Filter):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def get_name():
        return 'sin'
    
    @staticmethod
    def apply(box: Box, output_file: str = None):
        out = Filter.create_video_writer(output_file, box.fps, box.window)
        frames = box.frames
        a = 2 * math.pi / box.shape[1]
        for i in range(frames):
            im = np.zeros((box.shape[0], box.shape[1], box.shape[2]), dtype=np.uint8)
            for j in range(box.shape[1]):
                rad = a * j + 2 * i * math.pi / frames
                t = (math.sin(rad) + 1) * (frames - 1) / 2
                im[:, j, :] = box[:, j, :, int(t)]
            im = cv2.resize(im, box.window)
            out.write(im)
        out.release()