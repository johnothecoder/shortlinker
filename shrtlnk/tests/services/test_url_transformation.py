from django.test import RequestFactory, TestCase, override_settings

from shrtlnk.models import ShortLink, ShortLinkClick
from shrtlnk.services.url_transformation import DestinationTransformer


@override_settings(SHORTLINK_CLICK_ID_PARAM="click_id")
class DestinationTransformerTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.transformer = DestinationTransformer()

    def create_click(
        self,
        destination_url: str = "https://example.com/destination",
    ) -> ShortLinkClick:
        short_link = ShortLink.objects.create(
            name="Example link",
            slug="example",
            destination_url=destination_url,
        )

        return ShortLinkClick.objects.create(
            link=short_link,
            ip_address="203.0.113.10",
            incoming_url="https://short.example/example/",
            meta_data={},
        )

    def test_returns_destination_without_existing_query_string(self) -> None:
        click = self.create_click()
        request = self.factory.get("/example/")

        destination = self.transformer.final_destination(click, request)

        self.assertEqual(
            destination,
            f"https://example.com/destination?click_id={click.id}",
        )

    def test_preserves_incoming_query_parameters(self) -> None:
        click = self.create_click()
        request = self.factory.get(
            "/example/",
            {
                "utm_source": "newsletter",
                "utm_campaign": "summer",
            },
        )

        destination = self.transformer.final_destination(click, request)

        self.assertEqual(
            destination,
            (
                "https://example.com/destination"
                f"?utm_source=newsletter"
                f"&utm_campaign=summer"
                f"&click_id={click.id}"
            ),
        )

    def test_preserves_destination_query_parameters(self) -> None:
        click = self.create_click(
            "https://example.com/destination"
            "?product=widgets&utm_source=website"
        )
        request = self.factory.get("/example/")

        destination = self.transformer.final_destination(click, request)

        self.assertEqual(
            destination,
            (
                "https://example.com/destination"
                "?product=widgets"
                "&utm_source=website"
                f"&click_id={click.id}"
            ),
        )

    def test_destination_query_overrides_incoming_query(self) -> None:
        click = self.create_click(
            "https://example.com/destination?utm_source=destination"
        )
        request = self.factory.get(
            "/example/",
            {
                "utm_source": "incoming",
            },
        )

        destination = self.transformer.final_destination(click, request)

        self.assertEqual(
            destination,
            (
                "https://example.com/destination"
                "?utm_source=destination"
                f"&click_id={click.id}"
            ),
        )

    def test_click_id_overrides_incoming_and_destination_values(self) -> None:
        click = self.create_click(
            "https://example.com/destination?click_id=fake-destination-id"
        )
        request = self.factory.get(
            "/example/",
            {
                "click_id": "fake-incoming-id",
            },
        )

        destination = self.transformer.final_destination(click, request)

        self.assertEqual(
            destination,
            (
                "https://example.com/destination"
                f"?click_id={click.id}"
            ),
        )

    def test_preserves_blank_destination_query_values(self) -> None:
        click = self.create_click(
            "https://example.com/destination?utm_content="
        )
        request = self.factory.get("/example/")

        destination = self.transformer.final_destination(click, request)

        self.assertEqual(
            destination,
            (
                "https://example.com/destination"
                "?utm_content="
                f"&click_id={click.id}"
            ),
        )

    def test_preserves_url_fragment(self) -> None:
        click = self.create_click(
            "https://example.com/destination?foo=bar#pricing"
        )
        request = self.factory.get("/example/")

        destination = self.transformer.final_destination(click, request)

        self.assertEqual(
            destination,
            (
                "https://example.com/destination"
                "?foo=bar"
                f"&click_id={click.id}"
                "#pricing"
            ),
        )

    @override_settings(SHORTLINK_CLICK_ID_PARAM="tracking_reference")
    def test_uses_configured_click_id_parameter_name(self) -> None:
        click = self.create_click()
        request = self.factory.get("/example/")

        destination = self.transformer.final_destination(click, request)

        self.assertEqual(
            destination,
            (
                "https://example.com/destination"
                f"?tracking_reference={click.id}"
            ),
        )