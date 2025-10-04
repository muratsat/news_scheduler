from typing import Literal

from django.utils import timezone
from ninja import ModelSchema, Schema

from .models import Article

Status = Literal["scheduled", "published", "archived"]


class ArticleSchema(ModelSchema):
    status: str

    class Meta:
        model = Article
        fields = ["id", "title", "content", "published_date", "archived_date"]

    @staticmethod
    def resolve_status(obj) -> Status:
        current_date = timezone.now()

        if current_date < obj.published_date:
            return "scheduled"

        if obj.archived_date is None or current_date <= obj.archived_date:
            return "published"

        return "archived"


class ArticleUpdateSchema(Schema):
    archived: bool
