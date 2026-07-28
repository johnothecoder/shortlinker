from urllib.parse import parse_qsl, urlencode, urlparse

from django.conf import settings
from django.http.request import HttpRequest

from shrtlnk.models import ShortLinkClick


class DestinationTransformer:
    # Hehe... Final Destination... still though, this is where we
    # ACTUALLY send the user, maintaining the query string and adding
    # our click ID (using whatever name the config dictates)
    def final_destination(
        self, short_link_click: ShortLinkClick, request: HttpRequest
    ) -> str:

        # Could've done something complicated here, didn't...
        # We have essentially up to 3 queries we're going to merge (in priority order)
        # 1. Stuff we want to decorate with (click_id)
        # 2. From the URL destination (short_link.destination_url)
        # 3. From the URL hit (the short link)
        # Why? Because I don't fancy handling utm whatever on every link when I could just, not

        parsed_destination = urlparse(short_link_click.link.destination_url)
        incoming_query = {key: value for key, value in request.GET.items()}
        destination_query = dict(
            parse_qsl(
                parsed_destination.query,
                keep_blank_values=True,
            )
        )

        combined_query = {
            **incoming_query,
            **destination_query,
            settings.SHORTLINK_CLICK_ID_PARAM: str(short_link_click.id),
        }

        return parsed_destination._replace(
            query=urlencode(combined_query),
        ).geturl()
