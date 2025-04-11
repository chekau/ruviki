
from dataclasses import dataclass

@dataclass
class Article:
     title: str
     content: str
     anotation: str 
     image: str| None = None
     id: int | None = None
     
    
