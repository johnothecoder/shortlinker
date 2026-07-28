from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from shrtlnk.models import ShortLink, ShortLinkClick


class ShortLinkClickTests(TestCase):
    def setUp(self) -> None:
        self.short_link = ShortLink.objects.create(
            name="Example link",
            slug="example",
            destination_url="https://example.com/destination",
        )

    def create_click(self, **kwargs) -> ShortLinkClick:
        values = {
            "link": self.short_link,
            "incoming_url": "https://short.example/example/",
        }
        values.update(kwargs)
        return ShortLinkClick.objects.create(**values)

    def test_creating_click_increments_link_total_clicks(self) -> None:
        self.assertEqual(self.short_link.total_clicks, 0)
        self.create_click()
        self.short_link.refresh_from_db()
        self.assertEqual(self.short_link.total_clicks, 1)

    def test_creating_multiple_clicks_increments_total_clicks(self) -> None:
        self.create_click()
        self.create_click()
        self.create_click()

        self.short_link.refresh_from_db()

        self.assertEqual(self.short_link.total_clicks, 3)

    def test_updating_existing_click_does_not_increment_total_clicks(self) -> None:
        click = self.create_click()

        self.short_link.refresh_from_db()
        self.assertEqual(self.short_link.total_clicks, 1)

        click.outbound_url = "https://example.com/changed"
        click.save()

        self.short_link.refresh_from_db()

        self.assertEqual(self.short_link.total_clicks, 1)

    def test_click_is_available_through_related_name(self) -> None:
        click = self.create_click()

        self.assertEqual(
            list(self.short_link.clicks.all()),
            [click],
        )

    def test_deleting_link_deletes_its_clicks(self) -> None:
        click = self.create_click()
        click_id = click.pk

        self.short_link.delete()

        self.assertFalse(ShortLinkClick.objects.filter(pk=click_id).exists())

    def test_meta_data_defaults_to_empty_dictionary(self) -> None:
        click = self.create_click()

        self.assertEqual(click.meta_data, {})

    def test_clicks_do_not_share_meta_data_dictionary(self) -> None:
        first_click = self.create_click()
        second_click = self.create_click()

        first_click.meta_data["browser"] = "Firefox"

        self.assertEqual(second_click.meta_data, {})

    def test_latitude_must_not_be_greater_than_90(self) -> None:
        click = ShortLinkClick(
            link=self.short_link,
            incoming_url="https://short.example/example/",
            latitude=Decimal("90.000001"),
        )

        with self.assertRaises(ValidationError):
            click.full_clean()

    def test_latitude_must_not_be_less_than_minus_90(self) -> None:
        click = ShortLinkClick(
            link=self.short_link,
            incoming_url="https://short.example/example/",
            latitude=Decimal("-90.000001"),
        )

        with self.assertRaises(ValidationError):
            click.full_clean()

    def test_longitude_must_not_be_greater_than_180(self) -> None:
        click = ShortLinkClick(
            link=self.short_link,
            incoming_url="https://short.example/example/",
            longitude=Decimal("180.000001"),
        )

        with self.assertRaises(ValidationError):
            click.full_clean()

    def test_longitude_must_not_be_less_than_minus_180(self) -> None:
        click = ShortLinkClick(
            link=self.short_link,
            incoming_url="https://short.example/example/",
            longitude=Decimal("-180.000001"),
        )

        with self.assertRaises(ValidationError):
            click.full_clean()

    def test_location_accuracy_cannot_be_negative(self) -> None:
        click = ShortLinkClick(
            link=self.short_link,
            incoming_url="https://short.example/example/",
            location_accuracy=-0.1,
        )

        with self.assertRaises(ValidationError):
            click.full_clean()

    def test_valid_location_passes_validation(self) -> None:
        click = ShortLinkClick(
            link=self.short_link,
            incoming_url="https://short.example/example/",
            latitude=Decimal("52.570316"),
            longitude=Decimal("-0.240849"),
            location_accuracy=12.5,
        )

        click.full_clean()

    def test_string_representation_contains_slug(self) -> None:
        click = self.create_click()

        self.assertIn("example", str(click))
        self.assertIn("click at", str(click))
