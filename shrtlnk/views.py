from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import View
from .models import ShortLink
from shrtlnk.services.click_creation import ClickCreator
from shrtlnk.services.url_transformation import DestinationTransformer

class ShortLinkHitView(View):

    click_creator: ClickCreator | None = None
    destination_transformer: DestinationTransformer | None = None

    # I can explain this to you, but I can't understand it for you...
    def __init__(
            self,
            click_creator: ClickCreator,
            destination_transformer: DestinationTransformer,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.click_creator = click_creator
        self.destination_transformer = destination_transformer

    # Use the slug, get the ShortLink model, create a ShortLinkClick, figure out the
    # destination, save it, and send the user there
    def get(self, request: HttpRequest, slug: str,) -> HttpResponse:

        short_link = get_object_or_404(
            ShortLink,
            slug=slug,
            is_active=True,
        )
        click = self.click_creator.get_click(short_link=short_link, request=request)
        final_destination = self.destination_transformer.final_destination(
            short_link_click=click,
            request=request,
        )

        click.outbound_url = final_destination
        click.save()

        return redirect(final_destination)