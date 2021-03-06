# DeepDanbooruTAG

![deepdanbooru example](https://lainsafe.delegao.moe/files/163459649453158.png)

Interface for pre-trained machine learning model [DeepDanbooru](https://github.com/KichangKim/DeepDanbooru) with ability to read different formats of images and save the given data in json file. It also can be used as python module.

## Installation

```
python setup.py
```

## Usage

> Warning: The script will download the model on the first run

**From console:**

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

**As module:**

```python
from deepdanboorutag import deepdanboorutag

tags = deepdanboorutag.get_tags(path_to_image)
```