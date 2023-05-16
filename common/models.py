from dataclasses import dataclass, fields
from typing import List

@dataclass
class Media:
    url:str
    thumbnail: str = None
    title:str = None
    description: str=None

@dataclass
class MediaMetadata:
    items:List[Media]
    chat_id:str = None
    raw_src:str = None
    title:str = None
    description: str=None