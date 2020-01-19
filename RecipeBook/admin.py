from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category info', {'fields': ['name']})
    ]
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    actions = ['remove_associated_recipes']

    def remove_associated_recipes(self, request, queryset):
        for obj in queryset:
            recipes = Recipe.objects.filter(categories=obj)
            for recipe in recipes:
                recipe.delete()

    remove_associated_recipes.short_description = "Remove associated recipes"

    def get_queryset(self, request):
        queryset = Category.objects.all().order_by('name')
        return queryset


admin.site.register(Category, CategoryAdmin)
