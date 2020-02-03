from django.db import models

# Create your models here.
class Search(models.Model):
    id = models.AutoField(primary_key=True)
    SearchQuery = models.CharField(max_length=180)