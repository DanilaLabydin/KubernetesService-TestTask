from typing import Annotated, Union
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks
import time
import os

from . import schemas

temp_storage = []


def write_file():
    with open("db/myfile.txt", 'w') as file:
        print("gdfgdg")
        file.write("test test test")
    # pass


def check_storage(storage, object_id):
    for object in storage:
        if object.get("id") == object_id:
            return False
        
    return True


def remove_object(storage, expire_time, object_id):
    time.sleep(expire_time)
    for object in storage:
        if object.get("id") == object_id:
            storage.remove(object)
            write_file(storage)


app = FastAPI()


@app.get("/metrics")
async def get_metrics():
    print(os.getcwd())
    print(os.listdir())
    write_file()
    print(os.listdir())
    return temp_storage


@app.put("/objects/{key}")
async def insert_object(key:int,
                        response_model: schemas.JsonObject,
                        background_tasks: BackgroundTasks,
                        Expires: Annotated[Union[int, None], Header()] = None):
    
    if check_storage(temp_storage, key) is False:
        raise HTTPException(status_code=400)
    
    if Expires:
        # run background task to delete object
        background_tasks.add_task(remove_object, storage=temp_storage, expire_time = Expires, object_id=key)
    
    json_object = {"id": key}
    json_object.update(response_model.dict())
    temp_storage.append(json_object)
    write_file(temp_storage)

    return json_object


@app.get("/objects/{key}")
async def get_object(key: int):
    for object in temp_storage:
        if object.get("id") == key:
            return object

    raise HTTPException(status_code=404)
