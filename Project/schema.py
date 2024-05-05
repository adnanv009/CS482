from ninja.orm import create_schema
from model import Podcast as PodcastModel
from model import PodcastCategory

Podcast = create_schema(PodcastModel)

class PodcastCategoryEnum(PodcastCategory):
    __schema__ = {"enum": [e.value for e in PodcastCategory]}
