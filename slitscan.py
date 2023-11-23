# convert images in image folder into a slitscan video expanded vertically

import argparse
import numpy as np
import os
import sys
import cv2

def calc_box(img, aspect, frames):
    h, w, c = img.shape
    window_size = (w, int(w / aspect))
    box_depth = max(w, frames)
    speed = (h - window_size[1]) / box_depth
    box = np.zeros((window_size[1], w, c, box_depth), dtype=np.uint8)
    for t in range(box_depth):
        offset = int(t * speed)
        box[:, :, :, t] = img[offset:offset + window_size[1], :, :]
    # save the result
    return box

files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image'))

for i, file in enumerate(files):
    if file.endswith('.png'):
        files[i] = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"image{os.sep}{file}")
    else:
        files[i] = None

files = list(filter(lambda x: x is not None, files))

WIDTH = 450
WINDOW_ASPECT = 16 / 9 # width / height
MAX_ASPECT = 10
MIN_ASPECT = 0.1
FRAME_RATE = 30 # fps
MOVIE_LENGTH = 10 # sec

if len(files) == 0:
    print('No image files found.')
    sys.exit(1)

args = argparse.ArgumentParser(description="a script designed to perform slit-scan processing on images stored in the 'image' folder. It sequentially processes each image, creating a slit-scan effect.")

args.add_argument('-w', '--width', help='width of the window', default=WIDTH)
args.add_argument('-a', '--aspect', help='aspect ratio of the window (float or fraction style) e.g. 16/9', default=WINDOW_ASPECT)
args.add_argument('-f', '--fps', help='frame rate', default=FRAME_RATE)
args.add_argument('-l', '--length', help='movie length (sec)', default=MOVIE_LENGTH)
args = args.parse_args()

width = args.width
try:
    width = int(width)
except ValueError:
    print('Invalid width.')
    sys.exit(1)

aspect = args.aspect
try:
    if type(aspect) == str and aspect.find('/') != -1:
        aspect = float(aspect.split('/')[0]) / float(aspect.split('/')[1])
    else:
        aspect = float(aspect)
except ValueError:
    print('Invalid aspect ratio.')
    sys.exit(1)

if aspect < MIN_ASPECT or MAX_ASPECT < aspect:
    print('aspect ratio must be between {} and {}'.format(MIN_ASPECT, MAX_ASPECT))
    sys.exit(1)

fps = args.fps
try:
    fps = int(fps)
except ValueError:
    print('Invalid frame rate.')
    sys.exit(1)

length = args.length
try:
    length = int(length)
except ValueError:
    print('Invalid movie length.')
    sys.exit(1)

frames = fps * length

for i, file in enumerate(files):
    basename = os.path.splitext(os.path.basename(file))[0]
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"video{os.sep}{basename}"), exist_ok=True)
    print("loading {}".format(file))
    img = cv2.imread(file)
    # resize image with keeping aspect ratio
    size = (width, img.shape[0] * width // img.shape[1])
    img = cv2.resize(img, size)
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"video{os.sep}{basename}{os.sep}box.npy")):
        box = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"video{os.sep}{basename}{os.sep}box.npy"))
        h, w, c = img.shape
        window_size = (w, int(w / aspect))
        box_depth = max(w, frames)
        shape = (window_size[1], w, c, box_depth)
        same_shape = True
        for i in range(len(shape)):
            if shape[i] != box.shape[i]:
                same_shape = False
                break

        if same_shape:
            print("box.npy found and compatible with the current settings. skipping...")
            continue
        else:
            print("box.npy is not compatible with the current settings. Recalculating...")
            box = calc_box(img, aspect, frames)
    else:
        print("box.npy not found. calculating...")
        box = calc_box(img, aspect, frames)
    
    print("box has been calculated. saving...")
    # save box
    np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"video{os.sep}{basename}{os.sep}box.npy"), box)

    print("box shape: {}".format(box.shape))

    # axis: 0, 1, 3
    window_size = (box.shape[1], box.shape[0]) # width, height
    filenames = ["y.mp4", "x.mp4", "t.mp4"]
    for _axis in range(3):
        print(f"creating {filenames[_axis]}...")
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"video{os.sep}{basename}{os.sep}{filenames[_axis]}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, fps, window_size)
        axis = _axis if _axis != 2 else 3
        for i in range(frames):
            k = int(i / frames * box.shape[axis])
            if axis == 0: # y axis
                # see t axis as y axis
                im = np.transpose(box[k, :, :, :], (2, 0, 1))
                im = cv2.resize(im, window_size)
            elif axis == 1: # x axis
                # see t axis as x axis
                im = np.transpose(box[:, k, :, :], (0, 2, 1))
                im = cv2.resize(im, window_size)
            elif axis == 3: # t axis
                im = cv2.resize(box[:, :, :, k], window_size)
            out.write(im)
        out.release()
        print(f"saved {filename}")

    # yaw
    filenames = ["yaw.mp4", "pitch.mp4", "roll.mp4"]
    axes = [[1, 3, 0], [3, 0, 1], [0, 1, 3]]
    for _axis in range(3):
        print(f"creating {filenames[_axis]}...")
        filename = filenames[_axis]
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"video{os.sep}{basename}{os.sep}{filename}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, fps, window_size)
        a1, a2, a3 = axes[_axis]
        min_w = min(box.shape[a1], box.shape[a2])
        min_h = int(min_w / aspect)
        if min_h > box.shape[a3]:
            min_h = box.shape[a3]
            min_w = int(min_h * aspect)
        middle = (box.shape[a1] // 2, box.shape[a2] // 2, box.shape[a3] // 2)
        min_mid = min(middle[0], middle[1])
        for i in range(frames):
            white = np.full((min_h, min_w, 3), 255, dtype=np.uint8)
            rad = np.radians(i / frames * 360)
            for k in range(min_w):
                radius = k - min_mid
                x = middle[0] + int(radius * np.cos(rad))
                y = middle[1] + int(radius * np.sin(rad))
                if x < 0 or x >= box.shape[a1] or y < 0 or y >= box.shape[a2]:
                    continue
                z_min = middle[2] - int(min_h / 2)
                z_max = middle[2] + int(min_h / 2)
                if z_max - z_min != min_h:
                    z_max += 1
                if _axis == 0:
                    white[:, k, :] = box[z_min:z_max, x, :, y]
                elif _axis == 1:
                    white[:, k, :] = box[y, z_min:z_max, :, x]
                elif _axis == 2:
                    white[:, k, :] = box[x, y, :, z_min:z_max].transpose(1, 0)
            im = cv2.resize(white, window_size)
            out.write(im)
        out.release()
        print(f"saved {filename}")
