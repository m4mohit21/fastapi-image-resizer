from fastapi import FastAPI, File, UploadFile
from PIL import Image
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

SIZES = {
    "300x250": (300, 250),
    "728x90": (728, 90),
    "160x600": (160, 600),
    "300x600": (300, 600)
}

def resize_image(file_path):
    image = Image.open(file_path)
    resized_files = []

    for name, size in SIZES.items():
        resized_img = image.resize(size)
        resized_path = f"{UPLOAD_DIR}/{name}.png"
        resized_img.save(resized_path)
        resized_files.append(resized_path)

    return resized_files

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    resized_images = resize_image(file_path)
    return {"message": "Images resized", "files": resized_images}
