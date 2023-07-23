#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import os
from importlib import import_module


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def __init__(self):
        """Initializes a FileStorage instance"""
        self.model_classes = {
            'BaseModel': import_module('models.base_model').BaseModel,
            'User': import_module('models.user').User,
            'State': import_module('models.state').State,
            'City': import_module('models.city').City,
            'Amenity': import_module('models.amenity').Amenity,
            'Place': import_module('models.place').Place,
            'Review': import_module('models.review').Review
        }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            filtered_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    filtered_dict[key] = value
            return filtered_dict

    def delete(self, obj=None):
        """Removes an object from the storage dictionary"""
        if obj is not None:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(obj_key, None)

    def new(self, obj):
        """Adds new object to storage dictionary"""
        obj_key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[obj_key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as file:
            temp = {k: v.to_dict() for k, v in self.__objects.items()}
            json.dump(temp, file)

    def reload(self):
        """Loads storage dictionary from file"""
        classes = self.model_classes
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, 'r') as file:
                temp = json.load(file)
                for key, val in temp.items():
                    class_name = val.get('__class__')
                    if class_name in classes:
                        obj = classes[class_name](**val)
                        self.new(obj)

    def close(self):
        """Closes the storage engine."""
        self.reload()

