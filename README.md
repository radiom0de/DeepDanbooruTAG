# DeepDanbooruTAG

![deepdanbooru example](https://lainsafe.delegao.moe/files/163459649453158.png)

Interface for pre-trained machine learning model “Deepdanbooru” with ability to read different formats of images and save the given data in json file. It also can be used as python module.

## Installation

```
python setup.py
```

> Warning: The script will download the model on the first run

## Usage

```
Usage:
  deepdanboorutag.py [-j] [--quiet | --verbose] <path_to_image_or_directory>
  deepdanboorutag.py (-h | --help)
  deepdanboorutag.py (-v | --version)

Options:
  -h --help     Show this screen.
  -v --version     Show version.
  -j --json     Place json file in image folder
  --quiet       Print less text
  --verbose     Print more text [default: True]
```