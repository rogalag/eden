import cv2
import numpy as np
from PIL import Image
from IPython.display import display


def show_image(img_in):
    img_pil = Image.fromarray(np.array(img_in))
    display(img_pil)


def cv2pil(cv2_img):
    # how to see if greyscale?
    if len(cv2_img.shape) == 2 or cv2_img.shape[2]==1:
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_GRAY2RGB)
    else:
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(cv2_img.astype('uint8'))
    return pil_img


def pil2cv(pil_img):
    pil_img = pil_img.convert('RGB') 
    cv2_img = np.array(pil_img) 
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
    cv2_img = cv2_img[:, :, ::-1].copy()
    return cv2_img
    