from django.db import models

# Create your models here.
class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    groups = models.ManyToManyField("Group")
    tasks = models.ManyToManyField("Task")
    class Meta():
        app_label='database'

class PC(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90)
    link = models.CharField(max_length=500)
    cpu = models.SmallIntegerField(default=1)
    gpu = models.SmallIntegerField(default=1)
    ram = models.SmallIntegerField(default=1)
    price = models.SmallIntegerField(default=0)
    class Meta():
        app_label='database'

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90)
    cpu = models.SmallIntegerField(default=1)
    gpu = models.SmallIntegerField(default=1)
    ram = models.SmallIntegerField(default=1)
    selected = models.BigIntegerField(default=0)
    class Meta():
        app_label='database'

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    selected = models.BigIntegerField(default=0)
    name = models.CharField(max_length=90)
    options = models.ManyToManyField(Task)
    class Meta():
        app_label='database'

class Email(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=240)
    email = models.EmailField()

class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=240)
    description = models.CharFeied(max_length=600)
    htmlFileName = models.CharField(max_length=50)