from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=90)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=512)
    salt = models.CharField(max_length=10)