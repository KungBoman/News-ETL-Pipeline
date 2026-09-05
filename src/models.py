from datetime import datetime
from typing import NotRequired, TypedDict


class Article(TypedDict):
    source: str
    title: str
    published_at: datetime
    text_url: str
    image_url: str | None
    summary: str | None
    author_name: str | None
    author_email: str | None
    category: NotRequired[str | None]
    is_politics_related: NotRequired[bool]
