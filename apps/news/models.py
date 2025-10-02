from django.db import models
from django.db.models import Q
from django.utils import timezone

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    published_date = models.DateTimeField(default=timezone.now)
    archived_date = models.DateTimeField(null=True, blank=True)

    @classmethod
    def published(cls):
        now = timezone.now()
        return cls.objects.filter(
            Q(archived_date__isnull=True) | Q(archived_date__gt=now),
            published_date__lte=now,
        )

    @classmethod
    def scheduled(cls):
        now = timezone.now()
        return cls.objects.filter(published_date__gt=now)

    @classmethod
    def archived(cls):
        now = timezone.now()
        return cls.objects.filter(archived_date__lte=now)

    def __str__(self):
        return self.title
