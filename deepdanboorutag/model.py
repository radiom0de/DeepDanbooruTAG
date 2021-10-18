import sys, os
import requests
import tempfile
import PIL
import numpy as np
import tensorflow as tf
from zipfile import ZipFile
from clint.textui import progress
import config

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
rootdir = os.path.dirname(__file__)



class DeepdanbooruModel():
    def __init__(self):
        self.model_url = config.model_url
        self.modeldir_path = os.path.join(rootdir, "model")
        self.model_path = os.path.join(rootdir, "model", "model-resnet_custom_v3.h5")
        self.model_sensevity = config.model_sensevity
        
        if not (os.path.exists(self.modeldir_path)):
            self.download_model()

        self.model = self.load_model()
        with open(os.path.join(self.modeldir_path, "tags.txt"), "r") as tags:
            self.tags = np.array([tag for tag in (tag.strip() for tag in tags) if tag])

    def download_model(self):
        os.mkdir(self.modeldir_path)
        temp_dir = tempfile.gettempdir()
        
        r = requests.get(self.model_url, stream=True)
        with open(os.path.join(temp_dir, "deepboorumodel.zip"), "wb") as tmp_zip:
            print("Downloading model...")
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    tmp_zip.write(chunk)
                    tmp_zip.flush()
            print("Model downloaded!")
        
        print("Extracting model...")
        with ZipFile(os.path.join(temp_dir, "deepboorumodel.zip")) as zf:
            zf.extractall(path=self.modeldir_path)
            print("Model extracted!")

    def load_model(self):
        print("Loading model...")
        model = tf.keras.models.load_model(self.model_path, compile=False)
        print("Model loaded!")
        return model
    
    def get_tags(self, img_path, verbose=True):
        try:
            img = np.array(PIL.Image.open(img_path).convert('RGB').resize((512, 512))) / 255.0
        except IOError:
            if verbose:
                print(f"Unsupported extension {img_path}")
            return 'fail', {}

        prediction = self.model.predict(np.array([img])).reshape(self.tags.shape[0])
        img_tags = {}
        for i in range(len(self.tags)):
            if prediction[i] > self.model_sensevity:
                img_tags[self.tags[i]] = float(prediction[i])

        return 'ok', img_tags
            

