from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class PodcastCategory(str, Enum):
    news = "News"
    sports = "Sports"
    entertainment = "Entertainment"
    science = "Science"
    health = "Health"
    business = "Business"
    technology = "Technology"
    national = "National"
    world = "World"
class Podcast(BaseModel):
    title: str
    description: str
    host: str
    publication_date: datetime
    category: PodcastCategory
    duration: int

