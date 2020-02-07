from django.db import models

# Create your models here.
class Example(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=360)
    class Meta():
        app_label='database'

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90)
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
