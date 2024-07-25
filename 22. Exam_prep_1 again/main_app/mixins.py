from django.db import models


class AwardedUpdatedMixin(models.Model):
    class Meta:
        abstract = True

    is_awarded = models.BooleanField(
        default=False
    )

    last_updated = models.DateTimeField(
        auto_now_add=True
    )
