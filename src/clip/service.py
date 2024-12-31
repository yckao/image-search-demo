import asyncio
from typing import List

from PIL import Image as PILImage
import torch
from transformers import CLIPModel, CLIPProcessor

from src.clip.exceptions import ClipGenerationError
from src.interfaces.clip import CLIPServiceProtocol


class CLIPService(CLIPServiceProtocol):
    model_name: str

    def __init__(self, model_name: str, model_path: str):
        self.model_name = model_name
        self.model = CLIPModel.from_pretrained(model_path)
        self.processor = CLIPProcessor.from_pretrained(model_path)

    def _image_embedding(self, image: PILImage) -> List[float]:
        image_input = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            embedding = self.model.get_image_features(**image_input)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
        return embedding[0].tolist()

    def _text_embedding(self, text: str) -> List[float]:
        text_input = self.processor(text=text, return_tensors="pt", padding=True)
        with torch.no_grad():
            embedding = self.model.get_text_features(**text_input)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
        return embedding[0].tolist()

    async def image_embedding(self, image: PILImage) -> List[float]:
        try:
            embedding = await asyncio.to_thread(self._image_embedding, image)
            return embedding
        except Exception as e:
            raise ClipGenerationError(detail=str(e)) from e

    async def text_embedding(self, text: str) -> List[float]:
        try:
            embedding = await asyncio.to_thread(self._text_embedding, text)
            return embedding
        except Exception as e:
            raise ClipGenerationError(detail=str(e)) from e
