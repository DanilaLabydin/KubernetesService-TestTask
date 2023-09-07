from typing import Annotated, Union
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
import time

from . import schemas

storage = []


def check_storage(key):
    for object in storage:
        if object.get("id") == key:
            return False
        
    return True


def test_background(expire, key):
    time.sleep(expire)
    for object in storage:
        if object.get("id") == key:
            storage.remove(object)


app = FastAPI()


@app.get("/metrics")
async def get_metrics():
    return storage


@app.put("/objects/{key}")
async def insert_object(key:int,
                        response_model: schemas.JsonObject,
                        background_tasks: BackgroundTasks,
                        Expires: Annotated[Union[int, None], Header()] = None):
    
    if check_storage(key) is False:
        raise HTTPException(status_code=400)
    
    if Expires:
        # run background task to delete object
        background_tasks.add_task(test_background, expire = Expires, key=key)
    
    json_object = {"id": key}
    json_object.update(response_model.dict())
    storage.append(json_object)

    return json_object


@app.get("/objects/{key}")
async def get_object(key: int):
    for object in storage:
        if object.get("id") == key:
            return object

    raise HTTPException(status_code=404)
