import os
import tempfile
import imageio
import eden.setup
from eden.canvas import *
from eden.utils import dataset


def run(params, delete_temp_files=True):
    neural_style = eden.setup.get_external_repo_dir('neural-style')
    content = params['content'] if 'content' in params else '%s/images/dog.jpg' % neural_style
    style = params['style'] if 'style' in params else '%s/images/starrynight.jpg' % neural_style
    output = params['output'] if 'output' in params else None
    init = params['init'] if 'init' in params else None
    init_type = 'image' if 'init' in params else 'random'
    content_weight = params['content_weight'] if 'content_weight' in params else 5
    style_weight = params['style_weight'] if 'style_weight' in params else 100
    tv_weight = params['tv_weight'] if 'tv_weight' in params else 0.001
    style_scale = params['style_scale'] if 'style_scale' in params else 1.0
    image_size = params['image_size'] if 'image_size' in params else 512
    num_iterations = params['num_iterations'] if 'num_iterations' in params else 500
    multi_gpu = params['multi_gpu'] if 'multi_gpu' in params else False
    init_image_str = (' -init_image %s' % init) if (init is not None and init_type=='image') else ''

    f_content = tempfile.NamedTemporaryFile(suffix='.png')
    f_style = tempfile.NamedTemporaryFile(suffix='.png')
    f_output = tempfile.NamedTemporaryFile(suffix='.png')  
    
    #use_temp_content = isinstance(content, str)
    if not isinstance(content, str):
        content.save(f_content.name, 'PNG')
        content = f_content.name
    else:
        f_content.close()

    if not isinstance(style, str):
        style.save(f_style.name, 'PNG')
        style = f_style.name
    else:
        f_style.close()
        
    if output is None:
        output = f_output.name
            
    cmd  = 'th %s/neural_style.lua' % neural_style
    cmd += ' -proto_file %s/models/VGG_ILSVRC_19_layers_deploy.prototxt' % neural_style
    cmd += ' -model_file %s/models/VGG_ILSVRC_19_layers.caffemodel' % neural_style
    cmd += ' -backend cudnn %s' % ('-cudnn_autotune' if not multi_gpu else '')
    cmd += ' -content_image %s' % content
    cmd += ' -style_image %s' % style
    cmd += ' -output_image %s' % output
    cmd += ' -init %s %s' % (init_type, init_image_str)
    cmd += ' -num_iterations %d' % num_iterations
    cmd += ' -image_size %d' % image_size
    cmd += ' -content_weight %0.4f' % content_weight
    cmd += ' -style_weight %0.4f' % style_weight
    cmd += ' -tv_weight %0.4f' % tv_weight
    cmd += ' -style_scale %0.4f' % style_scale
    cmd += ' -save_iter 0'
    cmd += ' -gpu %s -multigpu_strategy 3,6,12  ' % ('0' if not multi_gpu else '0,1,2,3')
    cmd += ' -lbfgs_num_correction %d' % (0 if not multi_gpu else 5)
    
    print(cmd)
    os.system(cmd)
    output_image = imageio.imread(output)
    
    if delete_temp_files:
        f_content.close()
        f_style.close()
        f_output.close()

    return output_image
    

    
def run_multires(params):
    neural_style = abraham.setup.get_external_repo_dir('neural-style')
    content = params['content'] if 'content' in params else '%s/images/dog.jpg' % neural_style
    style = params['style'] if 'style' in params else '%s/images/starrynight.jpg' % neural_style
    init = params['init'] if 'init' in params else None
    output = params['output'] if 'output' in params else 'output.png'
    image_size = params['image_size'] if 'image_size' in params else 2048
    content_weight = params['content_weight'] if 'content_weight' in params else 5
    style_weight = params['style_weight'] if 'style_weight' in params else 100
    tv_weight = params['tv_weight'] if 'tv_weight' in params else 0.001
    style_scale = params['style_scale'] if 'style_scale' in params else 1.0
    
    f_content = tempfile.NamedTemporaryFile(suffix='.png')
    f_style = tempfile.NamedTemporaryFile(suffix='.png')
    f_output = tempfile.NamedTemporaryFile(suffix='.png')  
    
    if not isinstance(content, str):
        content.save(f_content.name, 'PNG')
        content = f_content.name

    if not isinstance(style, str):
        style.save(f_style.name, 'PNG')
        style = f_style.name

    output_256 = tempfile.NamedTemporaryFile(suffix='.png')
    output_512 = tempfile.NamedTemporaryFile(suffix='.png')
    output_1024 = tempfile.NamedTemporaryFile(suffix='.png')

    params_256 = {
        'content': content,
        'style': style,
        'content_weight': content_weight,
        'style_weight': style_weight,
        'tv_weight': tv_weight,
        'style_scale': style_scale,
        'image_size': 256,
        'num_iterations': 1500}

    if init is not None:
        params_256['init'] = init

    params_512 = dict(params_256)
    params_1024 = dict(params_256)
    params_final = dict(params_256)
    
    params_512['image_size'] = 512
    params_1024['image_size'] = 1024
    params_final['image_size'] = image_size

    params_512['num_iterations'] = 1000
    params_1024['num_iterations'] = 600
    params_final['num_iterations'] = 300

    params_256['output'] = output_256.name
    params_512['output'] = output_512.name
    params_1024['output'] = output_1024.name

    params_512['init'] = output_256.name
    params_1024['init'] = output_512.name
    params_final['init'] = output_1024.name

    params_final['output'] = output
    params_final['multi_gpu'] = True
    
    img_out = run(params_256, delete_temp_files=False)
    img_out = run(params_512, delete_temp_files=False)
    img_out = run(params_1024, delete_temp_files=False)
    
    if params_final['image_size'] > params_1024['image_size']:
        img_out = run_neural_style(params_final)

    output_256.close()
    output_512.close()
    output_1024.close()
    f_content.close()
    f_style.close()
    f_output.close()

    return img_out

