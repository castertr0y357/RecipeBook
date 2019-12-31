from django.urls import path
from . import views

app_name = 'RecipeBook'
urlpatterns = [
    # ex: /
    path('', views.MainView.as_view(), name='main'),
    # ex: /Categories/
    path('Categories/', views.CategoryListView.as_view(), name='category_list'),
    # ex: /Categories/Beef/
    path('Categories/<category_name>/', views.CategoryDetailView.as_view(), name='category_detail'),
    # ex: /Categories/Beef/Steak
    path('Categories/<category_name>/<recipe_slug>/', views.RecipeDetailView.as_view(), name='view_recipe'),
    path('Categories/<category_name>/<path:recipe_slug>/', views.RecipeDetailView.as_view(), name='view_recipe'),
    # ex: /Categories/Beef/Steak/edit/
    path('Categories/<category_name>/<recipe_slug>/edit/', views.RecipeEditView.as_view(), name='edit_recipe'),
    path('Categories/<category_name>/<path:recipe_slug>/edit/', views.RecipeEditView.as_view(), name="edit_recipe"),
    # ex: /add_recipe/
    path('add_recipe/', views.RecipeAddView.as_view(), name='add_recipe'),
    # ex: /shopping_list/
    path('shopping_list/', views.ShoppingListView.as_view(), name='shopping_list'),
    # ex: /meal_planner/
    path('meal_planner/', views.MealPlannerView.as_view(), name='meal_planner'),
]
