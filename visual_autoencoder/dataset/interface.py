SITE_DATASET_DIR = "../dataset/sites/"
import os
import json

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)
    
import json
from matplotlib import pyplot as plt
from PIL import Image as PILImage
import numpy as np

def find_metadata_file(entries):
    metadata_filename = list(filter(lambda s: s.endswith(".json"), entries))
    if len(metadata_filename) == 0:
        raise FileNotFoundError("*.json")
    if len(metadata_filename) > 1:
        raise RuntimeError("There should be only 1 json file in each directory")
    return metadata_filename[0]

class Image:
    def __init__(self, path, name):
        self.name = name
        self._path = path
        self._entries = os.listdir(path)
        metadata_filename = find_metadata_file(self._entries)
        metadata_file = os.path.join(path, metadata_filename)
        self.metadata = read_json(metadata_file)
        data_filename = os.path.basename(self.metadata["img"])
        self._data_file = os.path.join(path, data_filename)
    
    @property
    def data(self,):
        return np.array(PILImage.open(self._data_file))
    
    def __repr__(self, ):
        return "<Image \"%s\">" % self.name

class Group:
    def __init__(self, path, name):
        self.name = name
        self._path = path
        self._entries = os.listdir(path)
        metadata_filename = find_metadata_file(self._entries)
        metadata_path = os.path.join(path, metadata_filename)
        self.metadata = read_json(os.path.join(metadata_path))
        self.images_dirs = list(filter(lambda image_id: os.path.isdir(os.path.join(self._path, image_id)) and image_id[0] != ".", self._entries))
        self._images = {}

    def __getitem__(self, item):
        if item in self._images:
            return self._images[item]
        if type(item) is str:
            if item not in self.images_dirs:
                raise KeyError(item)
            image_dir = item
        elif type(item) is int:
            image_dir = self.images_dirs[item]
        else:
            raise ValueError(item)
        
        image = Image(os.path.join(self._path, image_dir), os.path.join(self.name, image_dir))
        self._images[image_dir] = image
        return image
    
    def __repr__(self, ):
        return "<Group \"%s\">" % self.name
        
class Site:
    def __init__(self, path, DATASET_DIR=SITE_DATASET_DIR):
        self._path = os.path.join(DATASET_DIR, path)
        self._entries = os.listdir(self._path)
        self.metadata = None
        self._parse_metadata()
        self.name = self.metadata["title"]
        self.group_dirs = list(filter(lambda group_id: os.path.isdir(os.path.join(self._path, group_id)) and group_id[0] != ".", self._entries))
        self._groups = {}
    
    def __getitem__(self, item):
        if item in self._groups:
            return self._groups[item]
        if type(item) is str:
            if item not in self.group_dir:
                raise KeyError(item)
            group_dir = item
        elif type(item) is int:
            group_dir = self.group_dirs[item]
        else:
            raise ValueError(item)
        
        group = Group(os.path.join(self._path, group_dir), name=os.path.join(self.name, group_dir))
        self._groups[group_dir] = group
        return group
    
    def _parse_metadata(self, ):
        metadata_filename = find_metadata_file(self._entries)
        metadata_path = os.path.join(self._path, metadata_filename)
        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)
    
    def __repr__(self,):
        return "<Site \"%s\">" % self.metadata["title"]