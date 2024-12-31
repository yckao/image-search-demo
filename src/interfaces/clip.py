from typing import List, Protocol

from PIL import Image as PILImage


class CLIPServiceProtocol(Protocol):
    async def image_embedding(self, image: PILImage) -> List[float]: ...

    async def text_embedding(self, text: str) -> List[float]: ...
