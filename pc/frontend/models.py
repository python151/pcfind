from django.db import models

# Create your models here.
class Presets(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512)
    description = models.CharField(max_length=2048)
