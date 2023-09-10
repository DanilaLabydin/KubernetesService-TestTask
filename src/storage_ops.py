import os
import json
import logging


LOGGER = logging.getLogger(__name__)
EMPTY_STORAGE = {"objects": []}
STORAGE_PATH = "storage/objects.json"
OBJECTS_KEY = "objects"


def save_objects(storage):
    with open(STORAGE_PATH, "w") as file:
        try:
            file.write(json.dumps(storage))
            return True

        except TypeError as e:
            LOGGER.error(
                f"Error occured when you tried to save objects in the storage: {e}"
            )
            return False


def load_json_objects():
    if not os.path.isfile(STORAGE_PATH):
        return EMPTY_STORAGE

    with open(STORAGE_PATH, "r") as file:
        try:
            data = json.load(file)
            if len(data) == 0:
                LOGGER.info(f"Loaded storage is an empty file, set default storage.")
                return EMPTY_STORAGE

            json_objects = data.get(OBJECTS_KEY)

            if json_objects is None:
                LOGGER.error(
                    f"Wrong {STORAGE_PATH} file structure: not 'objects' key, watch storage_example.json, set empty storage."
                )
                return EMPTY_STORAGE

            if not isinstance(json_objects, list):
                LOGGER.error(
                    f"Wrong {STORAGE_PATH} file structure: not lists in the 'objects' key, watch storage_example.json, set empty storage."
                )
                return EMPTY_STORAGE

            return data

        except TypeError as e:
            LOGGER.error(
                f"Error occured when you tried to load objects from {STORAGE_PATH} file, set empty storage: {e}"
            )
            return EMPTY_STORAGE


def find_duplicated_id(temp_storage, object_id):
    for object in temp_storage[OBJECTS_KEY]:
        if object.get("id") == object_id:
            return True

    return False
