from .filter import Filter
import sys
sys.path.append('../')
from utils.box import Box
import cv2
import numpy as np
import os

class TimeWave(Filter):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def get_name():
        return 'timewave'
    
    @staticmethod
    def apply(box: Box, output_file: str = None):
        out = Filter.create_video_writer(output_file, box.fps, box.window)
        frames = box.frames
        a = frames / (box.shape[1] / 2)
        for i in range(frames):
            im = np.zeros((box.shape[0], box.shape[1], box.shape[2]), dtype=np.uint8)
            k = int(i / frames * box.shape[3])
            for j in range(box.shape[1]):
                t = a * j + 2 * i
                q = t // frames
                if q % 2 == 0:
                    t = t - q * frames
                else:
                    t = frames - (t - q * frames) - 1
                im[:, j, :] = box[:, j, :, int(t)]
            im = cv2.resize(im, box.window)
            out.write(im)
        out.release()