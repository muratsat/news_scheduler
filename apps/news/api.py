from typing import Literal

from django.db.models import Q
from django.utils import timezone
from ninja import ModelSchema, Router

from .models import Article

news_router = Router(tags=["News"])


class ArticleSchema(ModelSchema):
    class Meta:
        model = Article
        fields = ["id", "title", "content", "published_date", "archived_date"]


@news_router.get("/articles", response=list[ArticleSchema])
def list_articles(request, status: Literal["scheduled", "published", "archived"]):

    if status == "published":
        articles = Article.published()
    elif status == "scheduled":
        articles = Article.scheduled()
    elif status == "archived":
        articles = Article.archived()

    return articles
