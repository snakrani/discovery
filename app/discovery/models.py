from django.db import models


class CachePage(models.Model):
    url = models.URLField(max_length=2083, null=False, unique=True)
    count = models.BigIntegerField(null=True, default=0)
