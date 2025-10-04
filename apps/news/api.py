from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Router

from .models import Article
from .schemas import ArticleSchema, ArticleUpdateSchema, Status

news_router = Router(tags=["News"])


@news_router.get("/articles", response=list[ArticleSchema])
def list_articles(request, status: Status):

    if status == "scheduled":
        articles = Article.scheduled()
    elif status == "archived":
        articles = Article.archived()
    else:
        articles = Article.published()

    return articles


@news_router.get("/articles/{id}", response=ArticleSchema)
def get_article(request, id: int):
    article = get_object_or_404(Article, pk=id)
    return article


@news_router.patch("/articles/{id}")
def update_articles(request, id: int, body: ArticleUpdateSchema):
    article = get_object_or_404(Article, pk=id)

    article.archived_date = (
        (article.archived_date or timezone.now()) if body.archived else None
    )
    article.save()
