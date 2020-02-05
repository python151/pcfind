from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=512)
    password = models.CharField(max_length=512)
    salt = models.SmallIntegerField()
    pepper = models.SmallIntegerField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=50)
    birthDate = models.CharField(max_length=10)
    class Meta():
        app_label='database.models'
