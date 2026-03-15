from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from typing import List


app = FastAPI()

@app.post("/files")
async def upload_file(uploaded_file: UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(f"new_{filename}", "wb") as f:
        f.write(file.read())

    return {"success": True}

@app.post("/many_files")
async def upload_file(uploaded_files: List[UploadFile] = File(...)):
    for i, uploaded_file in enumerate(uploaded_files):
        file = uploaded_file.file
        filename = uploaded_file.filename
        with open(f"{i}_{filename}", "wb") as f:
            f.write(file.read())
    return {"success": True}

def iterfile(filename: str):
    with open(filename, "rb") as file:
        while chunk := file.read(1024 * 1024):
            yield chunk

@app.get("files/streaming/{filename}")
async def get_streaming_file(filename: str):
    return StreamingResponse(iterfile(filename), media_type="video/mp4")


@app.get("/files/filename")
async def get_file(filename: str):
    return FileResponse(filename)
