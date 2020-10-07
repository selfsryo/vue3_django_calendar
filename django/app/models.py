from django.db import models


class Holiday(models.Model):
    name = models.CharField('祝日', max_length=100)
    date = models.DateField('日付')

    def __str__(self):
        return self.name
