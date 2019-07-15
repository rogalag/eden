import os
import glob
from imutils import video
import numpy as np
import random
from PIL import Image
import cv2

from eden.utils import processing


class ImageLoader:

    def __init__(self):
        pass

    def load_image(self, path):
        frame_name = os.path.splitext(os.path.basename(path))[0]
        img_data = Image.open(path).convert("RGB")
        img = {'path': path, 'name': frame_name, 'data': img_data} 
        return img
    
    def load_directory(self, input_src, max_images=None, shuffle=False, recursive=False):
        self.input_src = input_src
        allowable_ext = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif']
        if recursive:
            self.images = [{'path':os.path.join(input_src, f)} for f in glob.glob('%s/**'%input_src, recursive=True) 
                           if os.path.isfile(os.path.join(input_src, f))
                           and os.path.splitext(f)[1].lower() in allowable_ext]
        else:
            self.images = [{'path':os.path.join(input_src, f)} for f in os.listdir(input_src) 
                           if os.path.isfile(os.path.join(input_src, f))
                           and os.path.splitext(f)[1].lower() in allowable_ext]
        self.images = sorted(self.images, key = lambda img: img['path']) 
        self.images = [self.images[f] for f in self.get_subset(max_images, len(self.images), shuffle)]
        self.is_movie = False
        
    def load_movie(self, input_src, max_images=None, shuffle=False):
        self.cap = cv2.VideoCapture(input_src)
        #fps = video.FPS().start()
        self.num_images = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.images = [{'frame': f} for f in self.get_subset(max_images, self.num_images, shuffle)]
        self.is_movie = True

    def get_subset(self, max_num_images, num_images, shuffle):
        num_samples = min(max_num_images if max_num_images is not None else 1e8, num_images)
        sort_order = random.sample(range(num_images), num_samples) if shuffle else sorted(range(num_samples))
        return sort_order

    def split(self, pct_test, train_dir=None, test_dir=None, shuffle=True):
        n = self.num_images()
        nt = int(pct_test * n)
        is_test = [ True if i<nt else False for i in range(n) ]
        random.shuffle(is_test)
        test_set = [self.images[i] for i in range(n) if is_test[i] ]
        train_set = [self.images[i] for i in range(n) if not is_test[i] ]
        train_dir = os.path.join(self.input_src, 'train') if train_dir is None else train_dir
        test_dir = os.path.join(self.input_src, 'test') if test_dir is None else test_dir
        if not os.path.isdir(train_dir):
            os.mkdir(train_dir)
        if not os.path.isdir(test_dir):
            os.mkdir(test_dir)
        for img in train_set:
            filename = os.path.split(img['path'])[-1]
            cmd = 'cp "%s" "%s" ' % (img['path'], os.path.join(train_dir, filename))
            os.system(cmd)
        for img in test_set:
            filename = os.path.split(img['path'])[-1]
            cmd = 'cp "%s" "%s" ' % (img['path'], os.path.join(test_dir, filename))
            os.system(cmd)
    
    def filter(self, criteria):
        self.get_info()
        if 'min_w' in criteria:
            self.images = [ f for f in self.images if f['w'] >= criteria['min_w'] ]
        if 'max_w' in criteria:
            self.images = [ f for f in self.images if f['w'] <= criteria['max_w'] ]
        if 'min_h' in criteria:
            self.images = [ f for f in self.images if f['h'] >= criteria['min_h'] ]
        if 'max_h' in criteria:
            self.images = [ f for f in self.images if f['h'] <= criteria['max_h'] ]  
        
    def get_info(self):
        for i in range(self.num_images()):
            img = self.get_image(i)
            self.images[i]['h'] = img['data'].height
            self.images[i]['w'] = img['data'].width

    def shuffle(self):
        random.shuffle(self.images)

    def num_images(self):
        return len(self.images)

    def get_image(self, index):
        if self.is_movie:
            idx_frame = self.images[index]['frame']
            self.cap.set(1, idx_frame)
            ret, img = self.cap.read()
            path = 'frame%06d' % (idx_frame+1)
            img_data = processing.cv2pil(img)
        else:
            path = self.images[index]['path']
            img_data = Image.open(img_path).convert("RGB")
        img = {'path': path, 'data': img_data} 
        return img
    



