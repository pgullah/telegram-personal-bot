# pyright: strict
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Media:
    url:str
    thumbnail: Optional[str] = None
    title:Optional[str] = None
    description: Optional[str] = None

@dataclass
class MediaMetadata:
    items:List[Media]
    chat_id:Optional[str] = None
    raw_src:Optional[str] = None
    title:Optional[str] = None
    description: Optional[str] =None
