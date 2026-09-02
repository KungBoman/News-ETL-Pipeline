from datetime import datetime
from typing import TypedDict


class Article(TypedDict):
    source: str
    title: str
    description: str | None
    url: str
    published_at: datetime
    author: str | None
    category: str | None
    is_politics_related: bool
