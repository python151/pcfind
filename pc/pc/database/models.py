from django.db import models

# Create your models here.
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=512)
    password = models.CharField(max_length=512)
    salt = models.SmallIntegerField()
    pepper = models.SmallIntegerField()
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=50)
    birthDate = models.CharField(max_length=10)
    class Meta():
        app_label='database.Admin'


class Example(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=180)
    class Meta():
        app_label='database'

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    examples = models.ManyToManyField(Example)
    groups = models.ManyToManyField("Group")
    class Meta():
        app_label='database'

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90)
    options = models.ManyToManyField(Task)
    class Meta():
        app_label='database'
