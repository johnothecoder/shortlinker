from unittest.mock import Mock

from django.http import Http404, HttpRequest
from django.test import RequestFactory, TestCase

from shrtlnk.models import ShortLink, ShortLinkClick
from shrtlnk.views import ShortLinkHitView


class ShortLinkHitViewTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        self.short_link = ShortLink.objects.create(
            name="Example link",
            slug="example",
            destination_url="https://example.com/destination",
        )

        self.click = ShortLinkClick.objects.create(
            link=self.short_link,
            incoming_url="https://short.example/c/example/",
            ip_address="203.0.113.10",
        )

        self.click_creator = Mock()
        self.destination_transformer = Mock()

        self.click_creator.get_click.return_value = self.click
        self.destination_transformer.final_destination.return_value = (
            "https://example.com/destination?click_id=test"
        )

        self.view = ShortLinkHitView.as_view(
            click_creator=self.click_creator,
            destination_transformer=self.destination_transformer,
        )

    def make_request(
        self,
        path: str = "/c/example/",
    ) -> HttpRequest:
        return self.factory.get(path)

    def test_active_short_link_redirects_to_final_destination(self) -> None:
        request = self.make_request()

        response = self.view(
            request,
            slug=self.short_link.slug,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            "https://example.com/destination?click_id=test",
        )

    def test_click_creator_receives_short_link_and_request(self) -> None:
        request = self.make_request()

        self.view(
            request,
            slug=self.short_link.slug,
        )

        self.click_creator.get_click.assert_called_once_with(
            short_link=self.short_link,
            request=request,
        )

    def test_destination_transformer_receives_click_and_request(
        self,
    ) -> None:
        request = self.make_request()

        self.view(
            request,
            slug=self.short_link.slug,
        )

        self.destination_transformer.final_destination.assert_called_once_with(
            short_link_click=self.click,
            request=request,
        )

    def test_final_destination_is_saved_on_click(self) -> None:
        request = self.make_request()

        self.view(
            request,
            slug=self.short_link.slug,
        )

        self.click.refresh_from_db()

        self.assertEqual(
            self.click.outbound_url,
            "https://example.com/destination?click_id=test",
        )

    def test_saving_outbound_url_does_not_increment_click_count_again(
        self,
    ) -> None:
        self.short_link.refresh_from_db()
        original_click_count = self.short_link.total_clicks

        request = self.make_request()

        self.view(
            request,
            slug=self.short_link.slug,
        )

        self.short_link.refresh_from_db()

        self.assertEqual(
            self.short_link.total_clicks,
            original_click_count,
        )

    def test_unknown_slug_returns_404(self) -> None:
        request = self.make_request("/c/unknown/")

        with self.assertRaises(Http404):
            self.view(
                request,
                slug="unknown",
            )

        self.click_creator.get_click.assert_not_called()
        self.destination_transformer.final_destination.assert_not_called()

    def test_inactive_short_link_returns_404(self) -> None:
        self.short_link.is_active = False
        self.short_link.save()

        request = self.make_request()

        with self.assertRaises(Http404):
            self.view(
                request,
                slug=self.short_link.slug,
            )

        self.click_creator.get_click.assert_not_called()
        self.destination_transformer.final_destination.assert_not_called()
