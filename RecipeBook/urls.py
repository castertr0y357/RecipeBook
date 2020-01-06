from django.urls import path
from . import views

app_name = 'RecipeBook'
urlpatterns = [
    # ex: /
    path('', views.MainView.as_view(), name='main'),
    # ex: /Categories/
    path('Categories/', views.CategoryListView.as_view(), name='category_list'),
    # ex: /Categories/Beef/
    path('Categories/<slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('Categories/<path:slug>', views.CategoryDetailView.as_view(), name='category_detail'),
    # ex: /Recipes/
    path('Recipes/', views.RecipeListView.as_view(), name='recipe_list'),
    # ex: /Recipes/Grilled_Chicken/
    path('Recipes/<slug>/', views.RecipeDetailView.as_view(), name='view_recipe'),
    path('Recipes/<path:slug>/', views.RecipeDetailView.as_view(), name='view_recipe'),
    # ex: /Categories/Beef/Steak/edit/
    path('Recipes/<slug>/edit/', views.RecipeEditView.as_view(), name='edit_recipe'),
    path('Recipes/<path:slug>/edit/', views.RecipeEditView.as_view(), name="edit_recipe"),
    # ex: /add_recipe/
    path('add_recipe/', views.RecipeAddView.as_view(), name='add_recipe'),
    # ex: /shopping_list/
    path('shopping_list/', views.ShoppingListView.as_view(), name='shopping_list'),
    # ex: /meal_planner/
    path('meal_planner/', views.MealPlannerView.as_view(), name='meal_planner'),
    # ex: /search_results/
    path('search_results', views.SearchView.as_view(), name='search_results'),
]
