from fastapi import APIRouter, Depends, HTTPException
from fastapi import FastAPI, File, UploadFile

import aiofiles


router = APIRouter(
    prefix="/files",
    tags=["Files"],
    responses={404: {"description": "Not found"}},
)


# ---------------------------
# ----- Crud-Operations -----
# ---------------------------
@router.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    out_file_path = '/video/'+file.filename
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk
    return {"Result": "OK"}