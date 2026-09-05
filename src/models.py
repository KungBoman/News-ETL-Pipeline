from datetime import datetime
from typing import NotRequired, TypedDict


class Article(TypedDict):
    source: str
    title: str
    summary: str | None
    url: str
    published_at: datetime
    author: str | None
    category: str | None
    is_politics_related: NotRequired[bool]
