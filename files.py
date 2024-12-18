from fastapi import APIRouter 
from fastapi import UploadFile
from video_process import video_process

import aiofiles

import tensorflow as tf

import random

# model = tf.keras.models.load_model("model.keras")

router = APIRouter(
    prefix="/files",
    tags=["Files"],
    responses={404: {"description": "Not found"}},
)


@router.post("/predict")
async def create_upload_file(file: UploadFile):
    out_file_path = '/video/'+file.filename
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk
  
    return {"Result": random.randint(55,90)}
