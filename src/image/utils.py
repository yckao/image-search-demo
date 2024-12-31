import io
from typing import NamedTuple
from fastapi import File, HTTPException, UploadFile
from PIL import Image as PILImage, ImageFile


class IOFile(NamedTuple):
    filename: str
    file: io.BytesIO
    content_type: str


async def pil_image(file: UploadFile = File(...)) -> ImageFile:
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid mime type")
    try:
        image = PILImage.open(file.file)
        image.filename = file.filename
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file") from e


async def pil_image_to_io(image: ImageFile) -> IOFile:
    file = io.BytesIO()
    image_format = image.format or "PNG"
    image.save(file, format=image_format)
    file.seek(0)
    filename = image.filename or "untitled.png"

    return IOFile(
        filename=filename, file=file, content_type=f"image/{image_format.lower()}"
    )
