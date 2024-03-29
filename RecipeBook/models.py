from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    slug = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('RecipeBook:category_detail', args=[str(self.slug)])


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    ingredients_list = models.TextField(default="")
    servings = models.IntegerField(default=0, null=True, blank=True)
    prep_time = models.IntegerField(default=0, null=True, blank=True)
    cook_time = models.IntegerField(default=0, null=True, blank=True)
    directions = models.TextField(default="")
    source = models.CharField(max_length=100, default="", null=True, blank=True)
    notes = models.TextField(default="")
    categories = models.ManyToManyField(Category, blank=True)
    submitter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('RecipeBook:view_recipe', args=[str(self.slug)])


class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
