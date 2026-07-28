from django.urls import path

from shrtlnk.services.url_transformation import DestinationTransformer
from . import views
from .views import ShortLinkHitView
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
]