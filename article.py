
from dataclasses import dataclass



@dataclass
class User:
    name: str
    email:str


@dataclass
class Article:
     title: str
     content: str
     anotation: str 
     image: str| None = None
     views: int = 0
     id: int | None = None
     
    
