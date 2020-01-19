from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponseRedirect, reverse, redirect, render
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
    def post(request, *slug):
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
    def post(request, **slug):
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
    def post(request, *slug):
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


class BaseFormView(FormView):
    search = SearchForm

    def get_context_data(self, **kwargs):
        context = super(BaseFormView, self).get_context_data()

        context['form'] = self.search

        return context

    """
    @staticmethod
    def post(request):
        if request.method == 'POST':
            # print(True)
            form = SearchForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['search_name']
                base_url = reverse('RecipeBook:search_results')
                query_string = urlencode({'name': name})
                url = '{}?{}'.format(base_url, query_string)
                return HttpResponseRedirect(url)
            else:
                return HttpResponseRedirect(reverse('RecipeBook:main'))
    """

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
            category.recipes = Recipe.objects.filter(categories=category)

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
        for recipe in recipes:
            recipe.total_time = recipe.cook_time + recipe.prep_time
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
        for category in categories:
            category.recipes = Recipe.objects.filter(categories=category)

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

        category.recipes = Recipe.objects.filter(categories=category)

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


class RecipeAddView(BaseFormView):
    model = Recipe
    template_name = 'RecipeBook/add_recipe.html'
    context_object_name = 'recipe_add'
    queryset = None
    form_class = RecipeAddForm

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeAddView, self).get_context_data()

        context['recipe_add_form'] = RecipeAddForm(initial={'prep_time': '', 'cook_time': '', 'servings': ''})

        return context

    def post(self, request):
        if request.method == 'POST':
            search_form = SearchForm(request.POST)
            add_form = RecipeAddForm(request.POST)
            if add_form.is_valid():
                name = add_form.cleaned_data['recipe_name']
                ingredients_list = add_form.cleaned_data['ingredients_list']
                directions = add_form.cleaned_data['directions']
                servings = add_form.cleaned_data['servings']
                prep_time = add_form.cleaned_data['prep_time']
                cook_time = add_form.cleaned_data['cook_time']
                source = add_form.cleaned_data['source']
                categories = add_form.cleaned_data['category_input']
                categories_list = []

                if ',' in categories:
                    categories_parsed = categories.split(',')
                    for category in categories_parsed:
                        categories_list.append(category)
                else:
                    categories_list.append(categories)
                print(name, ingredients_list, directions, servings, prep_time, cook_time, source, categories)

                recipe = self.create_recipe(name, ingredients_list, directions, servings, prep_time, cook_time, source,
                                            categories_list)

                return redirect('RecipeBook:view_recipe', slug=recipe.slug)
            elif search_form.is_valid():
                name = search_form.cleaned_data['search_name']
                base_url = reverse('RecipeBook:search_results')
                query_string = urlencode({'name': name})
                url = '{}?{}'.format(base_url, query_string)
                return HttpResponseRedirect(url)
            else:
                return render('RecipeBook:add_recipe', {'form': add_form})

    def create_recipe(self, name, ingredients_list, directions, servings, prep_time, cook_time, source, categories):
        while True:
            try:
                recipe = Recipe.objects.create(name=name,
                                               ingredients_list=ingredients_list,
                                               directions=directions,
                                               servings=servings,
                                               prep_time=prep_time,
                                               cook_time=cook_time,
                                               source=source)
                break
            except db.utils.OperationalError:
                print("DB is locked")

        while True:
            try:
                recipe.slug = name + "-" + str(recipe.id)
                recipe.save()
                break

            except db.utils.OperationalError:
                print("DB is locked")

        # clean up categories
        recipe_categories = recipe.categories.all()
        for db_category in recipe_categories:
            recipe_categories.remove(db_category)

        for category in categories:
            try:
                db_category = Category.objects.get(name=category)
                recipe.categories.add(db_category)
            except Category.DoesNotExist:
                db_category = self.create_category(category)
                recipe.categories.add(db_category)

        return recipe

    @staticmethod
    def create_category(name):
        # strip extra spaces out of beginning and end of category name
        while name[0] == " ":
            name[0] = ""
        while name[-1] == " ":
            name[-1] = ""

        while True:
            try:
                db_category = Category.objects.create(name=name)
                break
            except db.utils.OperationalError:
                print("DB is locked")

        db_category.slug = name + "-" + str(db_category.id)

        while True:
            try:
                db_category.save()
                break
            except db.utils.OperationalError:
                print("DB is locked")
        return db_category


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
