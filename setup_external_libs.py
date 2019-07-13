import os
import zipfile
import eden.setup
from eden.utils import utils

                
eden.setup.set_external_repos_root("external")


# neural-style
neuralstyle = eden.setup.get_external_repo_dir("neural-style")
model_dir = os.path.join(neuralstyle, 'models')
model_files = [ ['https://gist.githubusercontent.com/ksimonyan/3785162f95cd2d5fee77/raw/bb2b4fe0a9bb0669211cf3d0bc949dfdda173e9e/VGG_ILSVRC_19_layers_deploy.prototxt', 'VGG_ILSVRC_19_layers_deploy.prototxt'],
    ['https://bethgelab.org/media/uploads/deeptextures/vgg_normalised.caffemodel', 'vgg_normalised.caffemodel'],
    ['http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_19_layers.caffemodel', 'VGG_ILSVRC_19_layers.caffemodel']
]
for url, filename in model_files:
    dest = os.path.join(model_dir, filename)
    if not os.path.exists(dest):
        cmd = 'wget -c --no-check-certificate %s -P %s' % (url, model_dir)
        os.system(cmd)

        
# setup deeplab-pytorch
file_id = '18kR928yl9Hz4xxuxnYgg7Hpi36hM8J2d'
deeplabpytorch = eden.setup.get_external_repo_dir("deeplab-pytorch")
dest_folder = os.path.join(deeplabpytorch, 'checkpoints')
dest_path = os.path.join(dest_folder, 'deeplabv2_resnet101_msc-cocostuff164k-100000.pth')
if not os.path.exists(dest_path):
    utils.try_make_folder(dest_folder)
    utils.download_file_from_google_drive(file_id, dest_path)


# setup stylegan
file_id = '1Kg7yqWSgoXN_mvHypX_fXt2GjrJZ_CZv'
stylegan = eden.setup.get_external_repo_dir("stylegan")
ckpt_folder = os.path.join(stylegan, 'checkpoints')
dest_folder = os.path.join(ckpt_folder, 'wikiarts')
dest_path = os.path.join(dest_folder, 'network-final-wikiarts.pkl')
if not os.path.exists(dest_path):
    utils.try_make_folder(ckpt_folder)
    utils.try_make_folder(dest_folder)
    utils.download_file_from_google_drive(file_id, dest_path)
    

# setup spade
spade = eden.setup.get_external_repo_dir("spade")
checkpoints_folder = os.path.join(spade, 'checkpoints')
dest_folder = os.path.join(checkpoints_folder, 'Labels2Landscapes_512')
ckpt_files = [
    ['1CXk6QPKeGLgp_VZwSUJFqnsvDuixx2fr', 'iter.txt'],
    ['1tsfDW8xb_Vat3En3hqVmoAQQBp8umNdV', 'latest_net_D.pth'],
    ['1T9FGxZQL9riB-a-cBOkFDdjBC2rf1Buh', 'latest_net_G.pth'],
    ['17dLGaO0l2oiAp7QVopON-yXw8DDs-M0e', 'loss_log.txt'],
    ['1b9n6RQN6GaSY8cvyZewM0xbNbAzJzGEF', 'opt.pkl'],
    ['1kgqOc4mlvOt1gjxrCchnSyzp_6NgJ6wX', 'opt.txt']
]
utils.try_make_folder(checkpoints_folder)
utils.try_make_folder(dest_folder)
for file_id, file_name in ckpt_files:
    dest_path = os.path.join(dest_folder, file_name)
    if not os.path.exists(dest_path):
        utils.download_file_from_google_drive(file_id, dest_path)


# setup densecap-tensorflow
file_id = '1yoJGXXpeSpQbU-6WpLsMXFLIka7xpTAy'
densecaptensorflow = eden.setup.get_external_repo_dir("densecap-tensorflow")
dest_folder = os.path.join(densecaptensorflow, 'output')
dest_path = os.path.join(dest_folder, 'ckpt.zip')
if not os.path.isdir(os.path.join(dest_folder, 'ckpt')):
    utils.try_make_folder(dest_folder)
    utils.download_file_from_google_drive(file_id, dest_path)
    zipf = zipfile.ZipFile(dest_path, 'r')
    zipf.extractall(dest_folder)
    zipf.close()
    os.system('rm %s' % dest_path)
