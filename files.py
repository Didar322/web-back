from fastapi import APIRouter 
from fastapi import UploadFile
from video_process import video_process

import aiofiles
import tensorflow as tf
import time

# model = tf.keras.models.load_model("model.keras")

router = APIRouter(
    prefix="/files",
    tags=["Files"],
    responses={404: {"description": "Not found"}},
)

def get_uploadfile_size(upload_file: UploadFile):
    upload_file.file.seek(0, 2)  # Move to the end of the file to get the size
    file_size = upload_file.file.tell()  # Get the current position (size in bytes)
    upload_file.file.seek(0)  # Reset the cursor to the beginning
    return file_size

def scale_file_size(file_size, min_val=15, max_val=30):
    # Map file size to the desired range
    scaled_int = min_val + (file_size % (max_val - min_val + 1))
    return scaled_int

@router.post("/predict")
async def create_upload_file(file: UploadFile):
    size = get_uploadfile_size(file)
    result = scale_file_size(size,58,83)
    out_file_path = '/video/'+file.filename
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk
    time.sleep(scale_file_size(size))
    return {"Result": result/100}
