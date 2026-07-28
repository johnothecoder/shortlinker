from django.http.request import HttpRequest

from shrtlnk.models import ShortLink, ShortLinkClick

# ShortLinkClick Creator...
class ClickCreator:
    def get_click(self, short_link: ShortLink, request: HttpRequest) -> ShortLinkClick:
        return ShortLinkClick.objects.create(
            link=short_link,
            ip_address=self.get_client_ip(request),
            incoming_url=request.build_absolute_uri(),
            meta_data={
                "user_agent": request.headers.get("User-Agent"),
                "referer": request.headers.get("Referer"),
                "accept_language": request.headers.get("Accept-Language"),
            },
        )

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str | None:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()

        return request.META.get('REMOTE_ADDR')