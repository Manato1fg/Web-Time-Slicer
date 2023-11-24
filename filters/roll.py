from .filter import Filter
import sys
sys.path.append('../')
from utils.box import Box
import cv2
import numpy as np
import os

class Roll(Filter):
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def get_name():
        return 'roll'
    
    @staticmethod
    def apply(box: Box, output_file: str = None):
        out = Filter.create_video_writer(output_file, box.fps, box.window)
        min_w = min(box.shape[0], box.shape[1])
        min_h = int(min_w / box.aspect)
        if min_h > box.shape[3]:
            min_h = box.shape[3]
            min_w = int(min_h * box.aspect)
        middle = (box.shape[0] // 2, box.shape[1] // 2, box.shape[3] // 2)
        min_mid = min(middle[0], middle[1])
        for i in range(box.frames):
            white = np.full((min_h, min_w, 3), 255, dtype=np.uint8)
            rad = np.radians(i / box.frames * 360)
            for k in range(min_w):
                radius = k - min_mid
                x = middle[0] + int(radius * np.cos(rad))
                y = middle[1] + int(radius * np.sin(rad))
                if x < 0 or x >= box.shape[0] or y < 0 or y >= box.shape[1]:
                    continue
                z_min = middle[2] - int(min_h / 2)
                z_max = middle[2] + int(min_h / 2)
                if z_max - z_min != min_h:
                    z_max += 1
                b = box[x, y, :, z_min:z_max]
                if b.shape[0] == white.shape[0]:
                    white[:, k, :] = b
                else:
                    white[:, k, :] = b.transpose(1, 0)
            im = cv2.resize(white, box.window)
            out.write(im)
        out.release()