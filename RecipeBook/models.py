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
    serving_size = models.IntegerField()
    directions = models.TextField()
    recipe_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.recipe_name
