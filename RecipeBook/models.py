from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    slug = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    ingredients_list = models.TextField()
    serving_size = models.IntegerField()
    directions = models.TextField()
    url = models.URLField()
    categories = models.ManyToManyField(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    slug = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name
