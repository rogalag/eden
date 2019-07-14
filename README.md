## Eden


> You were in Eden, the garden of God. Every kind of precious stone adorned you: ruby, topaz, and diamond, beryl, onyx, and jasper, sapphire, turquoise, and emerald. Your mountings and settings were crafted in gold, prepared on the day of your creation. 
> 
> Ezekiel 28:13


Eden is a sandbox for [the Abraham project](http://abraham.ai) to test pipelines for creating generative art with machine learning.

In Eden, Abraham is free of the autonomy, originality, and uniqueness requirements necessary to achieve an [autonomous artificial artist](https://medium.com/@genekogan/8384824a75c7). There are no security, privacy, or decentralization constraints. 

Once we eat from the tree of knowledge, admitting the possibility of evil (bias, subversion, data poisoning, collusion, and other potential attacks), all development will be transferred to [Abraham-mvp](https://github.com/abraham-ai/abraham), and Eden will be destroyed.


### Contents

Eden contains:
* wrappers of deep learning repositories for generative modeling, and manipulation of images, text, and audio, structured as [submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules).
* an API written on top to combine and chain models together.
* examples and demos.


### Setup

To install this library, command your terminal the following:

    git clone --recurse-submodules https://github.com/abraham-ai/eden
    cd eden
    pip install -r requirements.txt
    
A `Pipfile` is also provided if you wish to use [pipenv](https://github.com/pypa/pipenv).

The `external` folder contains submodules of dependencies. These can be used directly according to their own instructions, as well as through wrappers contained in the `eden` library. 

Many of the dependencies require additional files (mostly pre-trained models) to run. To install them, command:

    python setup_external_libs.py
    
The code is currently provided as-is. In the future, it should be turned into a [python package](https://pypi.org/).
    
### Examples

A set of work-in-progress examples are found inside the `examples` directory, packaged as Jupyter notebooks. In the future, it may make sense to divide these into "templates" (minimal examples that demonstrate how to use core features)
