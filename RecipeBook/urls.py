from django.urls import path
from . import views

app_name = 'RecipeBook'
urlpatterns = [
    # ex: /
    path('', views.MainView.as_view(), name='main'),
    # ex: /Beef/
    path('<category_name>/', views.CategoryView.as_view(), name='category'),
    # ex: /Beef/Steak
    path('<category_name>/<recipe_slug>', views.RecipeView.as_view(), name='view_recipe'),
    # ex: /Beef/Steak/edit/
    path('<category_name>/<recipe_slug>/edit/', views.RecipeEditView.as_view(), name='edit_recipe'),
    # ex: /add_recipe/
    path('add_recipe/', views.RecipeAddView.as_view(), name='add_recipe'),
    # ex: /shopping_list/
    path('shopping_list/', views.ShoppingListView.as_view(), name='shopping_list'),
    # ex: /meal_planner/
    path('meal_planner/', views.MealPlannerView.as_view(), name='meal_planner'),
]
