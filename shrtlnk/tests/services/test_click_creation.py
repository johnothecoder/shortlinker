from django.test import RequestFactory, TestCase, override_settings

from shrtlnk.models import ShortLink, ShortLinkClick
from shrtlnk.services.click_creation import ClickCreator


@override_settings(
    ALLOWED_HOSTS=[
        "testserver",
        "shrtlnkr.example",
    ]
)
class ClickCreatorTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.creator = ClickCreator()

        self.short_link = ShortLink.objects.create(
            name="Example link",
            slug="example",
            destination_url="https://example.com/destination",
        )

    def test_get_client_ip_uses_remote_addr(self) -> None:
        self.assertEqual(
            self.creator.get_client_ip(
                self.factory.get(
                    "/example/",
                    REMOTE_ADDR="192.168.1.10",
                )
            ),
            "192.168.1.10",
        )

    def test_get_client_ip_uses_first_forwarded_address(self) -> None:
        self.assertEqual(
            self.creator.get_client_ip(
                self.factory.get(
                    "/example/",
                    HTTP_X_FORWARDED_FOR="203.0.113.10, 10.0.0.1, 10.0.0.2",
                    REMOTE_ADDR="192.168.1.10",
                )
            ),
            "203.0.113.10",
        )

    def test_get_client_ip_strips_whitespace(self) -> None:
        self.assertEqual(
            self.creator.get_client_ip(
                self.factory.get(
                    "/example/",
                    HTTP_X_FORWARDED_FOR="  203.0.113.10  , 10.0.0.1",
                )
            ),
            "203.0.113.10",
        )

    def test_get_client_ip_returns_none_when_no_ip_is_available(self) -> None:
        request = self.factory.get("/example/")
        request.META.pop("REMOTE_ADDR", None)
        self.assertIsNone(self.creator.get_client_ip(request))

    def test_get_click_creates_click_from_request(self) -> None:
        request = self.factory.get(
            "/example/?utm_source=newsletter",
            HTTP_HOST="shrtlnkr.example",
            HTTP_USER_AGENT="Mozilla/5.0 Test Browser",
            HTTP_REFERER="https://google.com/",
            HTTP_ACCEPT_LANGUAGE="en-GB,en;q=0.9",
            HTTP_X_FORWARDED_FOR="203.0.113.10, 10.0.0.1",
        )

        click = self.creator.get_click(self.short_link, request)

        self.assertIsInstance(click, ShortLinkClick)
        self.assertIsNotNone(click.pk)

        click.refresh_from_db()

        self.assertEqual(click.link, self.short_link)
        self.assertEqual(click.ip_address, "203.0.113.10")
        self.assertEqual(
            click.incoming_url,
            "http://shrtlnkr.example/example/?utm_source=newsletter",
        )
        self.assertEqual(
            click.meta_data,
            {
                "user_agent": "Mozilla/5.0 Test Browser",
                "referer": "https://google.com/",
                "accept_language": "en-GB,en;q=0.9",
            },
        )

    def test_get_click_creates_database_record(self) -> None:
        request = self.factory.get(
            "/example/",
            REMOTE_ADDR="192.168.1.10",
        )

        self.assertEqual(ShortLinkClick.objects.count(), 0)

        click = self.creator.get_click(self.short_link, request)

        self.assertEqual(ShortLinkClick.objects.count(), 1)
        self.assertTrue(ShortLinkClick.objects.filter(pk=click.pk).exists())
