from django.urls import include, path

from shrtlnk.services.url_transformation import DestinationTransformer
from .views import ShortLinkHitView, home
from shrtlnk.services.click_creation import ClickCreator

urlpatterns = [
    path(
        "c/<slug:slug>/",
        ShortLinkHitView.as_view(
            click_creator=ClickCreator(),
            destination_transformer=DestinationTransformer(),
        ),
        name="follow-short-link",
    ),
    path("", home, name="home"),
]