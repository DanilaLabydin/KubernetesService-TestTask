import time
import logging

from typing import Annotated, Union
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
from prometheus_fastapi_instrumentator import Instrumentator

from . import schemas
from . import storage_ops


TEMP_STORAGE = storage_ops.load_json_objects()
LOGGER = logging.getLogger(__name__)


app = FastAPI()


Instrumentator().instrument(app).expose(app)
# sudo docker run -p 9090:9090 -v /home/danila/Documents/github_repos/KubernetesService-TestTask/prometheus_data/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus


def remove_object(temp_storage, expire_time, object_id):
    time.sleep(expire_time)
    for object in temp_storage["objects"]:
        if object.get("id") != object_id:
            continue

        temp_storage["objects"].remove(object)
        if storage_ops.save_objects(temp_storage) is False:
            LOGGER.error("Error occured in deleting expires object")


# @app.get("/metrics", tags=["Metrics"])
# async def get_metrics():
#     return


@app.get("/probes/liveness", tags=["Probes"])
async def liveness_probe():
    return


@app.get("/probes/readiness", tags=["Probes"])
async def readiness_probe():
    return


@app.put("/objects/{key}", status_code=201, tags=["Storage"])
async def insert_object(
    key: int,
    response_model: schemas.JsonObject,
    background_tasks: BackgroundTasks,
    Expires: Annotated[Union[int, None], Header()] = None,
):
    if storage_ops.find_duplicated_id(TEMP_STORAGE, key) is True:
        raise HTTPException(
            status_code=400, detail=f"Object with id {key} already exists"
        )

    if Expires:
        # run background task to delete object
        background_tasks.add_task(
            remove_object, temp_storage=TEMP_STORAGE, expire_time=Expires, object_id=key
        )

    json_object = {"id": key}
    json_object.update(response_model.dict())
    TEMP_STORAGE["objects"].append(json_object)
    storage_ops.save_objects(TEMP_STORAGE)

    return json_object


@app.get("/objects/{key}", status_code=200, tags=["Storage"])
async def get_object(key: int):
    for object in TEMP_STORAGE["objects"]:
        if object.get("id") == key:
            return object

    raise HTTPException(status_code=404, detail=f"Object with id {key} not found")
