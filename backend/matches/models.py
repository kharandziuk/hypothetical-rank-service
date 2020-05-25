from django.db import models


class Match(models.Model):
    name = models.CharField(max_length=255)
