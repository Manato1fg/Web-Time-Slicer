from cv2.typing import MatLike
import numpy as np
import math

class Box:
    def __init__(self, img: MatLike, aspect: float, fps: int, length: int, fast: bool = False):
        self.__img = img
        self.__aspect = aspect
        self.__fps = fps
        self.__length = length
        self.__frames = fps * length
        h, w, c = img.shape
        self.__window = (w, int(w / aspect)) # (width, height)
        self.__spf = float(h - self.__window[1]) / float(self.__frames) # scroll per frame
        self.__shape = (self.__window[1], self.__window[0], 3, self.__frames)
        self.__fast = fast
        self.fast_box = None
        if fast:
            self.fast_box = np.zeros(self.__shape, dtype=np.uint8)
            for i in range(self.__frames):
                self.fast_box[:, :, :, i] = self.__img[int(self.__spf * i):int(self.__spf * i) + self.__window[1], :, :]
    
    def save(self, output_file: str):
        np.save(output_file, self.__img)
    
    @staticmethod
    def load(input_file: str, size: tuple, aspect: float, fps: int, length: int, fast: bool = False):
        img = np.load(input_file)
        assert img.shape[0] == size[1] and img.shape[1] == size[0]
        return Box(img, aspect, fps, length, fast)
        
    def __getitem__(self, key: tuple) -> MatLike:
        assert len(key) == 4
        if self.__fast:
            return self.fast_box[key]
        y, x, _, t = key
        if type(t) == slice:
            t_start = t.start if t.start is not None else 0
            t_stop = t.stop if t.stop is not None else self.frames
            t_step = t.step if t.step is not None else 1
            if type(y) == slice:
                white = np.zeros((self.window[1], self.frames, 3), dtype=np.uint8)
                y_start = y.start if y.start is not None else int(self.spf) * t_start
                y_stop = y.stop if y.stop is not None else int(self.spf) * t_stop
                y_step = y.step if y.step is not None else int(self.spf) * t_step
                new_y = lambda i: range(y_start + i, y_stop + i, y_step)
                for i in range(self.window[1]):
                    white[i, :, :] = self.__img[new_y(i), x, :]
                return white
            else:
                white = np.zeros((int(t_stop - t_start) // t_step, self.window[0], 3), dtype=np.uint8)
                y_start = y + int(self.spf) * t_start
                y_stop = y + int(self.spf) * t_stop
                y_step = int(self.spf) * t_step
                new_y = range(y_start, y_stop, y_step)
                white[:, x, :] = self.__img[new_y, x, :]
                return white[:, x, :]
        else:
            if type(y) == slice:
                y_start = y.start if y.start is not None else 0
                y_stop = y.stop if y.stop is not None else self.window[1]
                y_step = y.step if y.step is not None else 1
                new_y = range(y_start + math.floor(t * self.spf), y_stop + math.floor(t * self.spf), y_step)
                return self.__img[new_y, x, :]
            else:
                return self.__img[math.floor(t*self.spf) + y, x, :]
    
    @property
    def shape(self):
        return self.__shape

    @property
    def window(self):
        return self.__window
    
    @property
    def fps(self):
        return self.__fps
    
    @property
    def frames(self):
        return self.__frames
    
    @property
    def spf(self):
        return self.__spf
    
    @property
    def aspect(self):
        return self.__aspect