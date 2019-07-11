import sys
import abraham.setup

import click
import cv2
from enum import Enum
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import yaml
import random
import glob
from tqdm import tqdm
from addict import Dict


class Config(Enum):
    cocostuff164k = 1
    cocostuff10k = 2

    
def get_classtable(LABELS):
    with open(LABELS) as f:
        classes = {}
        for label in f:
            label = label.rstrip().split("\t")
            classes[int(label[0])] = label[1].split(",")[0]
    return classes


def setup(config, cuda=True, crf=False):
    global CONFIG, device, classes, postprocessor, model, preprocessing, inference
    deeplab_pytorch = abraham.setup.get_external_repo_dir('deeplab-pytorch')
    sys.path.insert(0, deeplab_pytorch)
    from libs.models import DeepLabV2_ResNet101_MSC
    from libs.utils import DenseCRF
    from demo import get_device, setup_postprocessor, preprocessing, inference
    
    if config == Config.cocostuff164k:
        config_path = '%s/configs/cocostuff164k.yaml' % deeplab_pytorch
        model_path = '%s/checkpoints/deeplabv2_resnet101_msc-cocostuff164k-100000.pth' % deeplab_pytorch

    CONFIG = Dict(yaml.load(open(config_path, 'rb')))
    device = get_device(cuda)
    torch.set_grad_enabled(False)

    labels_file = "%s/%s" % (deeplab_pytorch, CONFIG.DATASET.LABELS)
    classes = get_classtable(labels_file)
    postprocessor = setup_postprocessor(CONFIG) if crf else None

    model = eval(CONFIG.MODEL.NAME)(n_classes=CONFIG.DATASET.N_CLASSES)
    state_dict = torch.load(model_path, map_location=lambda storage, loc: storage)
    model.load_state_dict(state_dict)
    model.eval()
    model.to(device)
    
    
def run(image):
    if isinstance(image, str):
        image = cv2.imread(image, cv2.IMREAD_COLOR)
    image, raw_image = preprocessing(np.array(image), device, CONFIG)
    labelmap = inference(model, image, raw_image, postprocessor)
    labels = np.unique(labelmap)
    return labelmap


def labelmap_as_image(labelmap, label=None):
    if label is not None:
        labelmap = 255 * (labelmap == label)
    labelmap = np.array([labelmap] * 3)
    labelmap = np.swapaxes(labelmap, 2, 0)
    labelmap = np.swapaxes(labelmap, 1, 0)
    labelmap = labelmap.astype(np.uint8)
    return labelmap

