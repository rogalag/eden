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
        img = {'name': frame_name, 'data': img_data} 
        return img
    
    def load_directory(self, input_src, max_images=None, shuffle=False, recursive=False):
        allowable_ext = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.gif']
        if recursive:
            self.images = [os.path.join(input_src, f) for f in glob.glob('%s/**'%input_src, recursive=True) 
                           if os.path.isfile(os.path.join(input_src, f))
                           and os.path.splitext(f)[1].lower() in allowable_ext]
        else:
            self.images = [os.path.join(input_src, f) for f in os.listdir(input_src) 
                           if os.path.isfile(os.path.join(input_src, f))
                           and os.path.splitext(f)[1].lower() in allowable_ext]
        self.images = sorted(self.images)
        self.all_frames = self.get_subset(max_images, len(self.images), shuffle)
        self.is_movie = False
        
        
    def load_movie(self, input_src, max_images=None, shuffle=False):
        self.cap = cv2.VideoCapture(input_src)
        #fps = video.FPS().start()
        self.num_images = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.all_frames = self.get_subset(max_images, self.num_images, shuffle)
        self.is_movie = True

    
    def get_subset(self, max_num_images, num_images, shuffle):
        num_samples = min(max_num_images if max_num_images is not None else 1e8, num_images)
        sort_order = random.sample(range(num_images), num_samples) if shuffle else sorted(range(num_samples))
        return sort_order

    
    def split():
        train=[]
        test=[]
    
    
    def filter():
        print('tbd')
    
    
    def get_image(self, index):
        idx_frame = self.all_frames[index]
        if self.is_movie:
            self.cap.set(1, idx_frame);
            ret, img = self.cap.read()
            frame_name = 'frame%06d' % (idx_frame+1)
            img_data = processing.cv2pil(img)
        else:
            img_path = self.images[idx_frame]
            frame_name = os.path.splitext(os.path.basename(img_path))[0]
            img_data = Image.open(img_path).convert("RGB")
        img = {'name': frame_name, 'data': img_data} 
        # isTrain = Trejkl
        return img
    
