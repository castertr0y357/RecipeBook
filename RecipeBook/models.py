from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.category_name


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    recipe_name = models.CharField(max_length=100)
    ingredients_list = models.TextField()
    directions = models.TextField()
    recipe_url = models.URLField()

    def __str__(self):
        return self.recipe_name
