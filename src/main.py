import time
import logging

from typing import Annotated, Union
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from prometheus_fastapi_instrumentator import Instrumentator

from . import schemas
from . import storage_ops


LOGGER = logging.getLogger(__name__)
TEMP_STORAGE = storage_ops.load_json_objects()
OBJECTS_KEY = storage_ops.OBJECTS_KEY


app = FastAPI()


Instrumentator().instrument(app).expose(app)


def remove_object(temp_storage, expire_time, object_id):
    time.sleep(expire_time)
    for object in temp_storage[OBJECTS_KEY]:
        if object.get("id") != object_id:
            continue

        temp_storage[OBJECTS_KEY].remove(object)
        if storage_ops.save_objects(temp_storage) is False:
            LOGGER.error(
                f"Error occurred in deleting the expired object with id: {object_id}."
            )


@app.get("/probes/liveness", status_code=200, tags=["Probes"])
async def liveness_probe():
    return "Liveness check succeeded."


@app.get("/probes/readiness", status_code=200, tags=["Probes"])
async def readiness_probe():
    return "Readiness check succeeded."


@app.put("/objects/{key}", status_code=201, tags=["Storage"])
async def insert_object(
    key: int,
    response_model: schemas.JsonObject,
    background_tasks: BackgroundTasks,
    Expires: Annotated[Union[int, None], Header()] = None,
):
    if storage_ops.find_duplicated_id(TEMP_STORAGE, key) is True:
        raise HTTPException(
            status_code=400, detail=f"Object with the ID {key} already exists."
        )

    if Expires:
        # run background task to delete object
        background_tasks.add_task(
            remove_object, temp_storage=TEMP_STORAGE, expire_time=Expires, object_id=key
        )

    json_object = {"id": key}
    json_object.update(response_model.dict())
    TEMP_STORAGE[OBJECTS_KEY].append(json_object)
    storage_ops.save_objects(TEMP_STORAGE)

    return json_object


@app.get("/objects/{key}", status_code=200, tags=["Storage"])
async def get_object(key: int):
    for object in TEMP_STORAGE[OBJECTS_KEY]:
        if object.get("id") == key:
            return object

    raise HTTPException(status_code=404, detail=f"Object with ID {key} not found.")
