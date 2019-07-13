## Eden


> You were in Eden, the garden of God; Every precious stone was your covering: The ruby, the topaz and the diamond; The beryl, the onyx and the jasper; The lapis lazuli, the turquoise and the emerald; And the gold, the workmanship of your settings and sockets, Was in you. 
> 
> Ezekiel 28:13


Eden is a sandbox for making art with machine learning. It is intended to be a testing ground for [Abraham](http://abraham.ai) which is free of the constraints necessary to achieve an [autonomous artificial artist](https://medium.com/@genekogan/8384824a75c7) (autonomy, originality, and uniqueness). 

It assumes the absence of evil (bias, collusion, and exploits), and thus does not implement any features toward security, privacy, or decentralization. It should be considered an innocent paradise of artificial art. Once we have eaten from the tree of knowledge, all development will be transferred to [Abraham-MVP](https://github.com/abraham-ai/abraham), and Eden will be destroyed.

### Contents

Eden contains:
* wrappers for various deep learning repositories for generative modeling, and manipulation of images, text, and audio, structured as [submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
* an API written on top to combine and chain models together.
* examples and demos using the API.


### Setup

To install this library, command your terminal the following:

    git clone --recurse-submodules https://github.com/abraham-ai/eden
    cd eden
    pip install -r requirements.txt
    
A `Pipfile` is also provided if you wish to use [pipenv](https://github.com/pypa/pipenv).

The `external` folder contains submodules of various libraries that act as dependencies. These can be used directly according to their own instructions, as well as through wrappers contained in the `eden` library. 

Many of the dependencies require additional files (mostly pre-trained models) to run. To install all of them, command your terminal:

    python setup_external_libs.py
    
Currently, the repo is packaged as-is. In the future, it should be turned into a proper python package.
    
### Examples

A set of work-in-progress examples are found inside the `examples` directory, packaged as Jupyter notebooks. In the future, it may make sense to divide these into "templates" (minimal examples that demonstrate how to use core features)
