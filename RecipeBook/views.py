from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponseRedirect, reverse,redirect
from django import db
from django.db import connection
from .models import Category, Recipe
from .forms import SearchForm, RecipeAddForm
from urllib.parse import urlencode


# ------------------------------------- Base Views ---------------------------------------------------------------------
class BaseListView(ListView):
    search = SearchForm

    def get_context_data(self, *args, **kwargs):
        context = super(BaseListView, self).get_context_data()

        context['form'] = self.search

        return context

    @staticmethod
    def post(request):
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['search_name']
                base_url = reverse('RecipeBook:search_results')
                query_string = urlencode({'name': name})
                url = '{}?{}'.format(base_url, query_string)
                return HttpResponseRedirect(url)
            else:
                raise ValidationError


class BaseDetailView(DetailView):
    search = SearchForm

    def get_context_data(self, **kwargs):
        context = super(BaseDetailView, self).get_context_data()

        context['form'] = self.search

        return context

    @staticmethod
    def post(request):
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['search_name']
                base_url = reverse('RecipeBook:search_results')
                query_string = urlencode({'name': name})
                url = '{}?{}'.format(base_url, query_string)
                return HttpResponseRedirect(url)
            else:
                raise ValidationError


class BaseUpdateView(UpdateView):
    search = SearchForm

    def get_context_data(self, **kwargs):
        context = super(BaseUpdateView, self).get_context_data()

        context['form'] = self.search

        return context

    @staticmethod
    def post(request):
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['search_name']
                base_url = reverse('RecipeBook:search_results')
                query_string = urlencode({'name': name})
                url = '{}?{}'.format(base_url, query_string)
                return HttpResponseRedirect(url)
            else:
                raise ValidationError


class BaseCreateView(CreateView):
    search = SearchForm

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data()

        context['form'] = self.search

        return context

    @staticmethod
    def post(request):
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['search_name']
                base_url = reverse('RecipeBook:search_results')
                query_string = urlencode({'name': name})
                url = '{}?{}'.format(base_url, query_string)
                return HttpResponseRedirect(url)
            else:
                raise ValidationError


# ------------------------------------- Main and Search Views ----------------------------------------------------------
class MainView(BaseListView):
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


class SearchView(BaseListView):
    model = Recipe
    template_name = 'RecipeBook/search_results.html'
    context_object_name = 'search_results'
    queryset = None

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data()

        name = self.request.GET.get('name')
        recipes = Recipe.objects.filter(name__icontains=name).order_by('name')
        form = self.search

        context['name'] = name
        context['recipes'] = recipes
        context['form'] = form

        return context


# ------------------------------------- Category views -----------------------------------------------------------------
class CategoryListView(BaseListView):
    model = Category
    template_name = 'RecipeBook/category_list.html'
    context_object_name = 'category_list'
    queryset = None

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        categories = Category.objects.all()

        context['categories'] = categories

        return context


class CategoryDetailView(BaseDetailView):
    model = Category
    template_name = 'RecipeBook/category_detail.html'
    context_object_name = 'category_recipe_list'
    queryset = None
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data()
        category = self.object

        category.recipes = Recipe.objects.filter(category=category)

        context['category'] = category

        return context


# ------------------------------------- Recipe views -------------------------------------------------------------------
class RecipeListView(BaseListView):
    model = Recipe
    template_name = 'RecipeBook/detail_page.html'
    queryset = None

    # only here to provide path for Recipes, no actual view is needed


class RecipeDetailView(BaseDetailView):
    model = Recipe
    template_name = 'RecipeBook/recipe_detail.html'
    context_object_name = 'recipe_view'
    queryset = None
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeDetailView, self).get_context_data()
        recipe = self.object
        recipe.ingredients = recipe.ingredients_list.split('\n')

        context['recipe'] = recipe

        return context


class RecipeEditView(BaseUpdateView):
    model = Recipe
    template_name = 'RecipeBook/edit_page.html'
    context_object_name = 'recipe_edit'
    queryset = None

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeEditView, self).get_context_data()
        recipe = self.object
        recipe.ingredients = recipe.ingredients_list.split('\n')

        context['recipe'] = recipe

        return context


class RecipeAddView(BaseCreateView):
    model = Recipe
    template_name = 'RecipeBook/add_recipe.html'
    context_object_name = 'recipe_add'
    queryset = None
    form_class = RecipeAddForm

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeAddView, self).get_context_data()

        context['recipe_add_form'] = RecipeAddForm(initial={'prep_time': '', 'cook_time': '', 'servings': ''})

        return context

    @staticmethod
    def add_recipe(request):
        if request.method == 'POST':
            form = RecipeAddForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                ingredients_list = form.cleaned_data['ingredients_list']
                directions = form.cleaned_data['directions']
                servings = form.cleaned_data['servings']
                prep_time = form.cleaned_data['prep_time']
                cook_time = form.cleaned_data['cook_time']
                url = form.cleaned_data['url']

                while True:
                    try:
                        recipe = Recipe.objects.create(name=name,
                                                       ingredients_list=ingredients_list,
                                                       directions=directions,
                                                       servings=servings,
                                                       prep_time=prep_time,
                                                       cook_time=cook_time,
                                                       url=url)
                        break
                    except db.utils.OperationalError:
                        print("DB is locked")

                while True:
                    try:
                        recipe.slug = name + "-" + str(recipe.id)
                        recipe.save()
                        return redirect('RecipeBook:view_recipe', slug=recipe.slug)

                    except db.utils.OperationalError:
                        print("DB is locked")

            else:
                raise ValidationError


# ------------------------------------- Shopping list and Meal planner views -------------------------------------------
class ShoppingListView(BaseListView):
    model = Recipe
    context_object_name = 'shopping_list'
    queryset = None

    def get_context_data(self, *args, **kwargs):
        context = super(ShoppingListView, self).get_context_data()

        return context


class MealPlannerView(BaseDetailView):
    model = Recipe
    context_object_name = 'meal_planner'
    queryset = None

    def get_context_data(self, *args, **kwargs):
        context = super(MealPlannerView, self).get_context_data()

        return context
