from django.db import models


class Link(models.Model):
    alias = models.CharField(max_length=256, null=False, blank=False, verbose_name='Alias', unique=True)
    link = models.URLField(null=False, blank=False, verbose_name='Link')

    def __str__(self):
        return f'https://linker24.herokuapp.com/{self.alias}'
