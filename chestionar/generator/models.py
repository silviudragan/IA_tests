from django.db import models

# Create your models here.


class Ontologie(models.Model):
    termen = models.CharField(max_length=200)
    parinte = models.CharField(max_length=200)
    relatie = models.CharField(max_length=100)

    def __str__(self):
        return self.termen