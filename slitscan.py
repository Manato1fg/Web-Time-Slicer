# convert images in image folder into a slitscan video expanded vertically

import argparse
import numpy as np
import os
import sys
import cv2
from filters import get_all_filter_names, get_filter_by_name
from utils.box import Box

# get image files
files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image'))

for i, file in enumerate(files):
    if file.endswith('.png'):
        files[i] = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"image{os.sep}{file}")
    else:
        files[i] = None

files = list(filter(lambda x: x is not None, files))

if len(files) == 0:
    print('No image files found.')
    sys.exit(1)

# settings
WIDTH = 450
WINDOW_ASPECT = 16 / 9 # width / height
MAX_ASPECT = 10
MIN_ASPECT = 0.1
FRAME_RATE = 30 # fps
MOVIE_LENGTH = 10 # sec

# parse arguments
args = argparse.ArgumentParser(description="a script designed to perform slit-scan processing on images stored in the 'image' folder. It sequentially processes each image, creating a slit-scan effect.")

args.add_argument('-w', '--width', help='width of the window', default=WIDTH)
args.add_argument('-a', '--aspect', help='aspect ratio of the window (float or fraction style) e.g. 16/9', default=WINDOW_ASPECT)
args.add_argument('-f', '--fps', help='frame rate', default=FRAME_RATE)
args.add_argument('-l', '--length', help='movie length (sec)', default=MOVIE_LENGTH)
args.add_argument('-fi', '--filter', help='filter name', default=None)
args.add_argument('--fast', help='fast mode (high memory usage)', action='store_true', default=False)
args = args.parse_args()

# validate arguments
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

filter_name = args.filter
if filter_name is None:
    fi = None
else:
    try:
        fi = get_filter_by_name(filter_name)
    except ValueError:
        print('Invalid filter name.')
        sys.exit(1)

# process for each image
for i, file in enumerate(files):
    basename = os.path.splitext(os.path.basename(file))[0]
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"video{os.sep}{basename}"), exist_ok=True)
    print("loading {}".format(file))
    img = cv2.imread(file)
    # resize image with keeping aspect ratio
    size = (width, img.shape[0] * width // img.shape[1])
    img = cv2.resize(img, size)

    # check if box.npy exists
    npy_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"video{os.sep}{basename}{os.sep}box.npy")
    if os.path.exists(npy_file):
        h, w, c = img.shape
        try:
            box = Box.load(npy_file, (w, h), aspect, fps, length, args.fast)
        except AssertionError:
            print("box.npy is not compatible with the current settings. Recalculating...")
            box = Box(img, aspect, fps, length, args.fast)
    else:
        print("box.npy not found. calculating...")
        box = Box(img, aspect, fps, length, args.fast)
    
    print("box has been calculated. saving...")
    # save box
    box.save(npy_file)

    print("box shape: {}".format(box.shape))

    # apply filter
    # if None is given, apply all filters
    if fi is None:
        for fil in get_all_filter_names():
            output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"video{os.sep}{basename}{os.sep}{fil}.mp4")
            print("applying {}...".format(fil))
            get_filter_by_name(fil).apply(box, output_file)
            print("done.")
    else:
        output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"video{os.sep}{basename}{os.sep}{fi.get_name()}.mp4")
        print("applying {}...".format(fi.get_name()))
        fi.apply(box, output_file)
        print("done.")
