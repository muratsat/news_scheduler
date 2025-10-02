from ninja import NinjaAPI

from apps.news.api import news_router

api = NinjaAPI()

api.add_router("/", news_router)
