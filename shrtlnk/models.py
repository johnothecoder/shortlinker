import uuid

from django.contrib.postgres.indexes import GinIndex
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import F


# This is a link, which is short
class ShortLink(models.Model):
    # PKs are good practice in DB design, Claude-ia told me so?
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Display name, because humans read words
    name = models.CharField(max_length=255)
    # In case you have to explain to Gary what this link is for
    notes = models.TextField(blank=True, null=True)
    # 32 chars would absolutely defeat the point, but in matters of taste...
    slug = models.SlugField(max_length=32, unique=True)
    # It's a URL, Steve
    destination_url = models.URLField()
    # Was going to do is_not_inactive, felt convoluted
    is_active = models.BooleanField(default=True)
    # Honestly if you're getting enough clicks to justify this size click counter, pay for bitly imo
    total_clicks = models.PositiveBigIntegerField(default=0)
    # At what time was thou link spawned into existence on the digital plane of existence...
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Short Link"
        verbose_name_plural = "Short Links"

    def __str__(self):
        return f"{self.name} ({self.slug})"


# A click, which belongs to a link, which is short
class ShortLinkClick(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.ForeignKey(ShortLink, on_delete=models.CASCADE, related_name="clicks")
    incoming_url = models.URLField()
    outbound_url = models.URLField(blank=True, null=True)
    # In some ungodly universe maybe IP lookup fails
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    # Primarily this platform is for poster QR code scanning, I'm expecting the client to ask for location
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ],
    )
    location_accuracy = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Estimated accuracy radius in metres",
    )
    location_captured_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    # Ah yes, "NoSQL" for when the schema description is "some data, I guess, probably"
    meta_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            # Someone, somewhere, will maybe do a query one day and go... aw, that's nice...
            GinIndex(
                fields=["meta_data"],
                name="click_meta_data_gin",
            ),
        ]
        verbose_name = "Hit"
        verbose_name_plural = "Hits"

    # Yes, I could've used a signal and done all the Redis and things...
    # But in the immortal words of Sgt Turner:
    # "You sure you wanna process all this lot? My pen's running out."
    # - Hot Fuzz (2007)
    # Seriously though, for low scale, this is fine. At high scale maybe should've
    # just sprung for some SaaS instead
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        with transaction.atomic():
            super().save(*args, **kwargs)
            if is_new:
                ShortLink.objects.filter(pk=self.link_id).update(
                    total_clicks=F("total_clicks") + 1
                )

    def __str__(self):
        return f"{self.link.slug} click at {self.created_at}"
