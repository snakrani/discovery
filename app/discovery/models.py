from django.db import models


class CachePage(models.Model):
    url = models.URLField(max_length=2083, null=False, unique=True, db_index=True)
    count = models.BigIntegerField(null=True, default=0, db_index=True)
