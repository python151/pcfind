from django.db import models

# Create your models here.
class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    class Meta:
        app_label = 'parts.models'
    def __str__(self):
        return self.name

class Feature(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=75)
    description = models.CharField(max_length=512)
    class Meta:
        app_label = 'parts.models'
    def __str__(self):
        return self.name

class Part(models.Model):
    PCPARTLIST = [
        ('mb', 'motherboard'),
        ('cs', 'case'),
        ('cp', 'CPU'),
        ('gp', 'GPU'),
        ('hd', 'HDD'),
        ('ss', 'SSD'),
        ('hy', 'hybrid drive'),
        ('cc', 'cpu cooler'),
        ('fn', 'fan'),
        ('rm', 'ram'),
        ('ps', 'PSU'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=20, choices=PCPARTLIST)
    link = models.CharField(max_length=512)
    class Meta:
        app_label = 'parts.models'
    def __str__(self):
        return self.name