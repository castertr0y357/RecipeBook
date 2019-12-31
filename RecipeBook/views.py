from django.views import generic
from .models import Category, Recipe


class MainView(generic.ListView):
    model = Category
    template_name = 'RecipeBook/main_page.html'
    context_object_name = 'categories'
    queryset = None

    def get_context_data(self, *args, **kwargs):
        context = super(MainView, self).get_context_data()
        categories = Category.objects.all().order_by('name')
        for category in categories:
            category.recipes = Recipe.objects.filter(category=category)

        context['categories'] = categories

        return context


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'RecipeBook/list_page.html'
    context_object_name = 'category_list'
    queryset = None

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        categories = Category.objects.all()

        context['categories'] = categories

        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'RecipeBook/list_page.html'
    context_object_name = 'category_recipe_list'
    queryset = None
    slug_field = 'category_name'
    slug_url_kwarg = 'category_name'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data()
        category = self.object

        recipes = Recipe.objects.filter(category=category)

        context['recipes'] = recipes

        return context


class RecipeDetailView(generic.DetailView):
    model = Recipe
    template_name = 'RecipeBook/detail_page.html'
    context_object_name = 'recipe_view'
    queryset = None
    slug_field = 'recipe_name'
    slug_url_kwarg = 'recipe_slug'

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeDetailView, self).get_context_data()
        recipe = self.object
        ingredients = recipe.ingredients_list.split('\n')

        context['recipe'] = recipe
        context['ingredients'] = ingredients

        return context


class RecipeEditView(generic.UpdateView):
    model = Recipe
    template_name = 'RecipeBook/edit_page.html'
    context_object_name = 'recipe_edit'
    queryset = None

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeEditView, self).get_context_data()
        recipe = self.object

        context['recipe'] = recipe

        return context


class RecipeAddView(generic.CreateView):
    model = Recipe
    template_name = 'RecipeBook/edit_page.html'
    context_object_name = 'recipe_add'
    queryset = None

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeAddView, self).get_context_data()
        recipe = self.object

        context['recipe'] = recipe

        return context


class ShoppingListView(generic.ListView):
    model = Recipe
    context_object_name = 'shopping_list'
    queryset = None


class MealPlannerView(generic.DetailView):
    model = Recipe
    context_object_name = 'meal_planner'
    queryset = None
