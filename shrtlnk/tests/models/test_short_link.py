from django.test import TestCase

from shrtlnk.models import ShortLink


class ShortLinkTests(TestCase):
    def test_total_clicks_defaults_to_zero(self) -> None:
        short_link = ShortLink.objects.create(
            name="Example link",
            slug="example",
            destination_url="https://example.com/",
        )

        self.assertEqual(short_link.total_clicks, 0)

    def test_link_is_active_by_default(self) -> None:
        short_link = ShortLink.objects.create(
            name="Example link",
            slug="example",
            destination_url="https://example.com/",
        )

        self.assertTrue(short_link.is_active)

    def test_string_representation(self) -> None:
        short_link = ShortLink.objects.create(
            name="Summer Campaign",
            slug="summer",
            destination_url="https://example.com/",
        )

        self.assertEqual(
            str(short_link),
            "Summer Campaign (summer)",
        )