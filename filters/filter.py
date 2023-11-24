import sys
sys.path.append('../')
from abc import abstractmethod
from utils.box import Box
import cv2

class Filter:
    def __init__(self):
        pass
    
    @abstractmethod
    def get_name():
        pass
    
    @abstractmethod
    def apply(box: Box, output_file: str):
        pass

    @staticmethod
    def create_video_writer(output_file: str, fps: int, size: tuple) -> cv2.VideoWriter:
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        return cv2.VideoWriter(output_file, fourcc, fps, size)