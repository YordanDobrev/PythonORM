from django.db import models


class IsAwarded(models.Model):
    class Meta:
        abstract = True

    is_awarded = models.BooleanField(
        default=False,
    )


class LastUpdated(models.Model):
    class Meta:
        abstract = True

    last_updated = models.DateTimeField(
        auto_now=True,
    )
