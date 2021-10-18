import sys
from setuptools import setup

setup(
    name="DeepDanbooruTAG",
    version="0.1",
    description="Interface for pre-trained machine learning model “Deepdanbooru” "
        "with ability to read different formats of images and save the given data "
        "in json file. It also can be used as python module.",
    author="radiomode",
    install_requires=[
        'numpy~=1.19.2',
        'pillow',
        'tensorflow==2.7.0rc0',
        'clint',
        'requests',
        'docopt'
    ],
)