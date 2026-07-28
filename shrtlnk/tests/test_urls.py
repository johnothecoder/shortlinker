from django.test import SimpleTestCase
from django.urls import resolve, reverse

from shrtlnk.views import ShortLinkHitView


class ShortLinkUrlTests(SimpleTestCase):
    def test_follow_short_link_url_reverses_correctly(self) -> None:
        url = reverse(
            "follow-short-link",
            kwargs={"slug": "summer-campaign"},
        )

        self.assertEqual(
            url,
            "/c/summer-campaign/",
        )

    def test_follow_short_link_url_resolves_to_correct_view(self) -> None:
        match = resolve("/c/summer-campaign/")

        self.assertIs(
            match.func.view_class,
            ShortLinkHitView,
        )
        self.assertEqual(
            match.kwargs,
            {"slug": "summer-campaign"},
        )