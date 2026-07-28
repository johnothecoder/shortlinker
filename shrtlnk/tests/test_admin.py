from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.test import RequestFactory, TestCase
from django.urls import reverse

from shrtlnk.admin import ShortLinkClickAdmin
from shrtlnk.models import ShortLink, ShortLinkClick


class ShortLinkClickAdminTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        self.model_admin = ShortLinkClickAdmin(
            ShortLinkClick,
            AdminSite(),
        )

        user_model = get_user_model()

        self.superuser = user_model.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-password",
        )

        self.short_link = ShortLink.objects.create(
            name="Example link",
            slug="example",
            destination_url="https://example.com/destination",
        )

        self.click = ShortLinkClick.objects.create(
            link=self.short_link,
            ip_address="203.0.113.10",
            incoming_url="https://short.example/example/?utm_source=test",
            outbound_url="https://example.com/destination?utm_source=test",
            meta_data={
                "user_agent": "Test Browser",
                "referer": "https://referrer.example/",
                "dangerous": "<script>alert('oops')</script>",
            },
        )

    def make_request(self) -> HttpRequest:
        request = self.factory.get("/")
        request.user = self.superuser

        return request

    def get_change_url(self) -> str:
        return reverse(
            "admin:shrtlnk_shortlinkclick_change",
            args=[self.click.pk],
        )

    def test_add_permission_is_denied(self) -> None:
        request = self.make_request()

        self.assertFalse(self.model_admin.has_add_permission(request))

    def test_change_permission_is_allowed(self) -> None:
        request = self.make_request()

        self.assertTrue(
            self.model_admin.has_change_permission(
                request,
                self.click,
            )
        )

    def test_delete_permission_is_denied(self) -> None:
        request = self.make_request()

        self.assertFalse(
            self.model_admin.has_delete_permission(
                request,
                self.click,
            )
        )

    def test_change_page_is_accessible(self) -> None:
        self.client.force_login(self.superuser)

        response = self.client.get(self.get_change_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.click.id))

    def test_change_page_hides_save_controls(self) -> None:
        self.client.force_login(self.superuser)

        response = self.client.get(self.get_change_url())

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'name="_save"')
        self.assertNotContains(response, 'name="_continue"')
        self.assertNotContains(response, 'name="_addanother"')
        self.assertNotContains(response, "deletelink")

    def test_pretty_meta_data_formats_json(self) -> None:
        rendered = str(self.model_admin.pretty_meta_data(self.click))

        self.assertIn("<pre", rendered)
        self.assertIn("&lt;script&gt;", rendered)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&quot;user_agent&quot;", rendered)
        self.assertIn("Test Browser", rendered)

    def test_click_cannot_be_changed_through_admin(self) -> None:
        self.client.force_login(self.superuser)

        original_incoming_url = self.click.incoming_url
        original_outbound_url = self.click.outbound_url

        response = self.client.post(
            self.get_change_url(),
            {
                "incoming_url": "https://evil.example/incoming",
                "outbound_url": "https://evil.example/outbound",
            },
        )

        # A valid admin POST normally redirects back to the changelist.
        self.assertEqual(response.status_code, 302)

        self.click.refresh_from_db()

        self.assertEqual(
            self.click.incoming_url,
            original_incoming_url,
        )
        self.assertEqual(
            self.click.outbound_url,
            original_outbound_url,
        )

    def test_all_displayed_database_fields_are_readonly(self) -> None:
        expected_readonly_fields = {
            "id",
            "link",
            "ip_address",
            "incoming_url",
            "outbound_url",
            "pretty_meta_data",
            "created_at",
        }

        self.assertEqual(
            set(self.model_admin.readonly_fields),
            expected_readonly_fields,
        )
