from django import forms
from django.contrib import admin
from django.utils import timezone

from .models import Article
from .schemas import Status

# Register your models here.


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"

    @staticmethod
    def resolve_status(obj) -> Status:
        now = timezone.now()

        if now < obj.published_date:
            return "scheduled"

        if obj.archived_date is None or now <= obj.archived_date:
            return "published"

        return "archived"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

    list_display = ("title", "published_date", "archived_date", "status")
    search_fields = ("title",)
    list_filter = ("created_at",)

    def status(self, obj):
        current_date = timezone.now()

        if current_date < obj.published_date:
            return "Scheduled"

        if obj.archived_date is None or current_date <= obj.archived_date:
            return "Published"

        return "Archived"
