from django.db import models
from django.utils import timezone


class CreatedAtUpdatedAtMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UrlShortener(CreatedAtUpdatedAtMixin):
    original_url = models.CharField(max_length=512, null=False, blank=False)
    shortened_url = models.CharField(max_length=255)
    counter = models.IntegerField(default=0)

    created_by = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "Url Shortener"
        verbose_name_plural = "Url Shorteners"
