import os
import sys
import pickle
import numpy as np
import tensorflow as tf
import PIL.Image
import random
import eden.setup


def setup(checkpoint_name):
    global Gs, fmt
    stylegan = eden.setup.get_external_repo_dir('stylegan')
    sys.path.insert(0, stylegan)

    import dnnlib
    import dnnlib.tflib as tflib
    import config

    fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
    tflib.init_tf()
    checkpoint_path = os.path.join(os.path.join(stylegan, 'checkpoints'), checkpoint_name)
    with open(checkpoint_path, 'rb') as file:
        G, D, Gs = pickle.load(file)
    

def run(input_z, truncation=1.0):
    latents = np.array(input_z).reshape((1, 512)) 
    #labels = np.zeros([latents.shape[0]] + Gs.input_shapes[1][1:])
    images = Gs.run(latents, None, truncation_psi=truncation, randomize_noise=False, output_transform=fmt)
    output = np.clip(images[0], 0, 255).astype(np.uint8)
    return output


