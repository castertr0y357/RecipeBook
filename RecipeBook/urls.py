from django.urls import path, include
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
    # ex: /Recipes/edit/
    path('Edit/', views.BaseUpdateView.as_view(), name='base_edit'),
    # ex: /Categories/Beef/Steak/edit/
    path('Edit/<slug>/', views.RecipeEditView.as_view(), name='edit_recipe'),
    path('Edit/<path:slug>/', views.RecipeEditView.as_view(), name='edit_recipe'),
    # ex: /add_recipe/
    path('add_recipe/', views.RecipeAddView.as_view(), name='add_recipe'),
    # ex: /shopping_list/
    path('shopping_list/', views.ShoppingListView.as_view(), name='shopping_list'),
    # ex: /meal_planner/
    path('meal_planner/', views.MealPlannerView.as_view(), name='meal_planner'),
    # ex: /search_results/
    path('search_results', views.SearchView.as_view(), name='search_results'),
    # --------------------------------Authentication---------------------------------------------
    # ex: /login/
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create_account/', views.CreateUserView.as_view(), name='create_user'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
]
