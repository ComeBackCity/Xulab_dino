#!/bin/bash 

set -x

conda create -n dino python=3.7 -y
conda activate dino
pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
pip install gdown
pip install opencv-python