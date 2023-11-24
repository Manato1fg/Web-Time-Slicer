from .filter import Filter
import sys
sys.path.append('../')
from utils.box import Box
import cv2
import numpy as np
import os
import math

class Tile(Filter):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def get_name():
        return 'tile'
    
    @staticmethod
    def apply(box: Box, output_file: str = None):
        out = Filter.create_video_writer(output_file, box.fps, box.window)
        frames = box.frames
        p = 5
        q = 2
        for i in range(frames):
            im = np.zeros((box.shape[0], box.shape[1], box.shape[2]), dtype=np.uint8)
            for l in range(p):
                for m in range(q):
                    if (l + m) % 2 == 0:
                        t = frames - 1 - i
                    else:
                        t = i
                    w = slice(box.shape[1] * l // p, box.shape[1] * (l + 1) // p)
                    h = slice(box.shape[0] * m // q, box.shape[0] * (m + 1) // q)
                    im[h, w, :] = box[h, w, :, t]
            im = cv2.resize(im, box.window)
            out.write(im)
        out.release()