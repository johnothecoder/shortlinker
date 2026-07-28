import json

from django.contrib import admin
from django.http import HttpRequest
from django.utils.html import format_html, escape
from django.utils.safestring import mark_safe

from shrtlnk.models import ShortLink, ShortLinkClick

@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination_url', 'slug', 'total_clicks')
    search_fields = ('name', 'destination_url', 'slug')
    list_filter = ('is_active',)

# For reference, we don't want to edit anything, just see it all (and beautify the JSON so it's readable)
@admin.register(ShortLinkClick)
class ShortLinkClickAdmin(admin.ModelAdmin):
    list_display = ('id', "link__slug", 'created_at')
    search_fields = ('incoming_url', 'outbound_url')
    list_filter = ("link__slug","created_at",)
    ordering = ("-created_at",)
    readonly_fields = (
        "id",
        "link",
        "ip_address",
        "pretty_meta_data",
        "created_at",
    )
    fields = (
        "id",
        "link",
        "ip_address",
        "incoming_url",
        "outbound_url",
        "pretty_meta_data",
        "created_at",
    )

    def has_add_permission(self, request) -> bool:
        return False

    # We can't edit anything... but we do want to see the "edit" page, so this is True
    def has_change_permission(self,request: HttpRequest, obj: ShortLinkClick | None = None,) -> bool:
        return True

    def has_delete_permission(self, request: HttpRequest, obj: ShortLinkClick | None = None,) -> bool:
        return False

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        # Hide the buttons
        extra_context.update({
            "show_save": False,
            "show_save_and_continue": False,
            "show_save_and_add_another": False,
            "show_delete": False,
        })

        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context,
        )

    @admin.display(description="Metadata")
    def pretty_meta_data(self, obj: ShortLinkClick) -> str:
        formatted_json = json.dumps(
            obj.meta_data,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        escaped_json = escape(formatted_json)
        return mark_safe(
            '<pre style="'
            'margin: 0; '
            'white-space: pre-wrap; '
            'overflow-wrap: anywhere;'
            f'">{escaped_json}</pre>'
        )