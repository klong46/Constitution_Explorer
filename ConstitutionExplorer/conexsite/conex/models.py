from django.db import models

class Constitution(models.Model):
    country = models.CharField(max_length=200)
    constitution_text = models.TextField(blank=True, default='')
    write_date = models.CharField(null=True, blank=True, default='', max_length=10)
    def __str__(self):
        return self.country
