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
    ingredients_list = models.TextField(default="")
    servings = models.IntegerField(default=0, null=True, blank=True)
    prep_time = models.IntegerField(default=0, null=True, blank=True)
    cook_time = models.IntegerField(default=0, null=True, blank=True)
    directions = models.TextField(default="")
    url = models.CharField(max_length=100, default="", null=True, blank=True)
    categories = models.ManyToManyField(Category, null=True, blank=True)
    slug = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name
