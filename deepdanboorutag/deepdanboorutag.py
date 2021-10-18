"""DeepDanbooruTAG.

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

"""

import os
import json
import model
import config
from docopt import docopt


def get_tags(model, path, verbose=True):
    tags = {}
    if (os.path.isfile(path)):
        tags[path] = model.get_tags(path)
    if (os.path.isdir(path)):
        for root, dirs, files in os.walk(path):
            for filename in files:
                imgpath = os.path.abspath(os.path.join(root, filename))
                status, imgtags = model.get_tags(imgpath, verbose)
                if (status == "ok"):
                    if verbose:
                        print(f"Getting tags for {imgpath}.")
                    tags[root+"/"+filename] = imgtags
    return tags


if __name__ == "__main__":
    args = docopt(__doc__, version="DeepDanbooruIO v0.1")
    
    path = args.get('<path_to_image_or_directory>')
    if not (os.path.exists(path)):
        print("Image of folder does not exist.")
        exit()
    verbose = not args.get('--quiet')    
    
    # Change current work dir
    if (os.path.isdir(path)):
        os.chdir(path)
    else:
        os.chdir(os.dirname(path))
    path = os.path.relpath(path, os.curdir)

    # Json
    if (args['--json']):
        json_path = config.json_data_filename
        if (os.path.isfile(path)):
            print("Json is only for dirs.")
            exit()
        data = {}

        # Load data if json already exists
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                try:
                    data = json.load(f)
                except:
                    data = {}

        with open(json_path, "w") as f:
            # Remove non-exist images
            if data:
                for img, tags in data.items():
                    if not (os.path.exists(img)):
                        data.pop(img)

            # Find new images
            new_images = set()
            for root, dirs, files in os.walk(path):
                for filename in files:
                    imgpath = root+"/"+filename
                    if imgpath not in data and os.path.basename(imgpath) != json_path:
                        new_images.add(imgpath)
            
            # Predict tags for new images
            if (len(new_images) > 0):
                print(f"{len(new_images)} new images detected. Model is going to load")
                model = model.DeepdanbooruModel()
                for image in new_images:
                    if verbose:
                        print(f"Getting tags for {image}")
                    status, imgtags = model.get_tags(image, verbose=verbose)
                    if (status == "ok"):
                        data[image] = imgtags
                print("Getting tags finished. Updating json...")
                json.dump(data, f)
                print("Data saved succefully!")
            else:
                print("No new images detected.")
    # Return string with image paths and tags
    else:
        model = model.DeepdanbooruModel()
        tags = get_tags(model, os.path.abspath(path), verbose=verbose)
        print(tags)

