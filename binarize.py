import numpy as np
import os
import cv2
import sys
import argparse
from tqdm import tqdm

def parse(parser):
    parser.add_argument('input', nargs='+', default=[], 
                        help='image file(s)')
    parser.add_argument('-o', '--outdir', required=True,
                        help='image output directory')
    parser.add_argument('-s', '--suffix', default='_bin',
                        help='suffix')
    parser.add_argument('-m', '--method', default='otsu',
                        choices=['otsu','bradley'],
                        help='binarization method')
    return parser.parse_args()

def bradley(img, size=30.0, t=25.0):
    # unfortunately quite slow right now :(
    ii = cv2.integral(img)
    r = int(size / 2)
    m = size % 2
    out = np.zeros(img.shape, np.uint8)    
    for y in tqdm(range(img.shape[0])):
    	for x in range(img.shape[1]):
            x1 = int(min(max(0, x - r), img.shape[1]))
            x2 = int(min(max(0, x + r+m), img.shape[1]))
            y1 = int(min(max(0, y - r), img.shape[0]))
            y2 = int(min(max(0, y + r+m), img.shape[0]))

            count = float((x2 - x1) * (y2 - y1))
            s = ii[y1,x1] - ii[y1, x2] - ii[y2, x1] + ii[y2, x2]

            if float(img[y,x]) >= (s * (100 - t) / 100) / count:
                out[y,x] = 255
    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parse(parser)
    
    for filename in tqdm(args.input): 
        img = cv2.imread(filename, cv2.IMREAD_COLOR)
        if img.ndim == 3:
            mean = np.mean(img, axis=2).astype(np.uint8)
        else:
            mean = img

        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
        mean = clahe.apply(mean)
        
        if args.method == 'otsu':
            _, binary = cv2.threshold(mean, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif args.method == 'bradley':
            binary = bradley(mean)
        else:
            raise ValueError('unknown method')

        basename = os.path.splitext(os.path.basename(filename))[0]
        out_fname = os.path.join(args.outdir, basename + args.suffix + '.png')
        cv2.imwrite(out_fname, binary)

