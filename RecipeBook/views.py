# Django imports
from django.views.generic import ListView, DetailView, FormView
from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponseRedirect, reverse, redirect, render
from django.db.models import Count, F
from django import db
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import AuthenticationForm

# Local imports
from .models import Category, Recipe
from .forms import SearchForm, RecipeForm
from .formatting import format_time
from urllib.parse import urlencode


# ------------------------------------- Base Views ---------------------------------------------------------------------
class BaseListView(ListView):
    search = SearchForm

    def get_context_data(self, *args, **kwargs):
        context = {'form': self.search}
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
        context = {'form': self.search}
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


class BaseUpdateView(FormView):
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


# ------------------------------------- Main and Search Views ----------------------------------------------------------
class MainView(BaseListView):
    model = Category
    template_name = 'RecipeBook/main_page.html'
    context_object_name = 'categories'
    queryset = None

    login_url = '/accounts/login/'

    def get_context_data(self, *args, **kwargs):
        context = super(MainView, self).get_context_data()
        categories = Category.objects.all()
        if categories.count() > 0:
            categories.recent = categories[categories.count() - 1]
        recipes = Recipe.objects.all()
        if recipes.count() > 0:
            recipes.recent = recipes[recipes.count() - 1]

        context['categories'] = categories
        context['recipes'] = recipes
        return context


class SearchView(BaseListView):
    model = Recipe
    template_name = 'RecipeBook/search_results.html'
    context_object_name = 'search_results'
    queryset = None

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data()
        name = self.request.GET.get('name')
        recipes = Recipe.objects.filter(name__icontains=name)
        for recipe in recipes:
            recipe.total_time = recipe.cook_time + recipe.prep_time
            if "http" in recipe.source:
                recipe.link = recipe.source
        form = self.search

        context['name'] = name
        context['recipes'] = recipes
        context['form'] = form
        return context

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            name = self.request.GET.get('name')
            sorting_method = self.request.GET.get('sorting_method')
            ascending = self.request.GET.get('ascending')
            data = []
            if ascending == "true":
                if sorting_method == "source":
                    query = None
                elif sorting_method == "total_time":
                    query = Recipe.objects.filter(name__icontains=name)\
                        .annotate(total_time=F('prep_time') + F('cook_time')).order_by('total_time')
                else:
                    query = Recipe.objects.filter(name__icontains=name)\
                        .annotate(total_time=F('prep_time') + F('cook_time')).order_by(sorting_method)
            elif ascending != "true":
                if sorting_method == "source":
                    query = None
                elif sorting_method == "total_time":
                    query = Recipe.objects.filter(name__icontains=name)\
                        .annotate(total_time=F('prep_time') + F('cook_time')).order_by('total_time').reverse()
                else:
                    query = Recipe.objects.filter(name__icontains=name)\
                        .annotate(total_time=F('prep_time') + F('cook_time')).order_by(sorting_method).reverse()
            else:
                query = None
                data = serialize('json', None)

            if query is not None:
                for obj in query:
                    url_link = '<a href="' + obj.get_absolute_url() + '">' + obj.name + '</a>'
                    if "http" in obj.source:
                        source = '<a href="' + obj.source + '">' + obj.source + '</a>'
                    else:
                        source = obj.source
                    json_data = {"name": url_link, "servings": obj.servings, "time": format_time(obj.total_time),
                                 "source": source}
                    data.append(json_data)

            return JsonResponse(data=data, safe=False)
        else:
            return render(self.request, self.template_name, context=self.get_context_data())


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

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            sorting_method = self.request.GET.get('sorting_method')
            ascending = self.request.GET.get('ascending')
            data = []
            if ascending == "true":
                if sorting_method == "recipe_count":
                    query = Category.objects.all().annotate(recipe_count=Count('recipe')).order_by('recipe_count')
                else:
                    query = Category.objects.all().annotate(recipe_count=Count('recipe')).order_by(sorting_method)
            elif ascending != "true":
                if sorting_method == "recipe_count":
                    query = Category.objects.all().annotate(recipe_count=Count('recipe')).order_by('recipe_count')\
                        .reverse()
                else:
                    query = Category.objects.all().annotate(recipe_count=Count('recipe')).order_by(sorting_method)\
                        .reverse()
            else:
                query = None
                data = serialize('json', None)

            if query is not None:
                for obj in query:
                    url_link = '<a href="' + obj.get_absolute_url() + '">' + obj.name + '</a>'
                    json_data = {"name": url_link, "recipe_count": obj.recipe_count}
                    data.append(json_data)

            return JsonResponse(data=data, safe=False)
        else:
            return render(self.request, self.template_name, context=self.get_context_data())


class CategoryDetailView(BaseDetailView):
    model = Category
    template_name = 'RecipeBook/category_detail.html'
    context_object_name = 'category_recipe_list'
    queryset = None
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data()
        category = self.get_object()
        category.recipes = Recipe.objects.filter(categories=category)
        for recipe in category.recipes:
            recipe.total_time = format_time(recipe.prep_time + recipe.cook_time)
            if "http" in recipe.source:
                recipe.link = recipe.source

        context['category'] = category
        return context

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            sorting_method = self.request.GET.get('sorting_method')
            ascending = self.request.GET.get('ascending')
            data = []
            if ascending == "true":
                if sorting_method == "source":
                    query = None
                elif sorting_method == "total_time":
                    query = Recipe.objects.filter(categories=self.get_object())\
                        .annotate(total_time=F('prep_time') + F('cook_time')).order_by('total_time')
                else:
                    query = Recipe.objects.filter(categories=self.get_object())\
                        .annotate(total_time=F('prep_time') + F('cook_time')).order_by(sorting_method)
            elif ascending != "true":
                if sorting_method == "source":
                    query = None
                elif sorting_method == "total_time":
                    query = Recipe.objects.filter(categories=self.get_object())\
                        .annotate(total_time=F('prep_time') + F('cook_time')).order_by('total_time').reverse()
                else:
                    query = Recipe.objects.filter(categories=self.get_object())\
                        .annotate(total_time=F('prep_time') + F('cook_time')).order_by(sorting_method).reverse()
            else:
                query = None
                data = serialize('json', None)

            if query is not None:
                for obj in query:
                    url_link = '<a href="' + obj.get_absolute_url() + '">' + obj.name + '</a>'
                    if "http" in obj.source:
                        source = '<a href="' + obj.source + '">' + obj.source + '</a>'
                    else:
                        source = obj.source
                    json_data = {"name": url_link, "servings": obj.servings, "time": format_time(obj.total_time),
                                 "source": source}
                    data.append(json_data)

            return JsonResponse(data=data, safe=False)
        else:
            return render(self.request, self.template_name, context=self.get_context_data())


# ------------------------------------- Recipe views -------------------------------------------------------------------
class RecipeListView(BaseListView):
    model = Recipe
    template_name = 'RecipeBook/recipe_list.html'
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
        recipe = self.get_object()
        recipe.ingredients = recipe.ingredients_list.split('\n')
        recipe.directions = recipe.directions.split('\n')
        recipe.prep_time = format_time(recipe.prep_time)
        recipe.cook_time = format_time(recipe.cook_time)

        if "http" in str(recipe.source):
            recipe.link = recipe.source

        context['recipe'] = recipe
        return context


class RecipeEditView(BaseDetailView):
    model = Recipe
    template_name = 'RecipeBook/edit_recipe.html'
    queryset = None
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    form_class = RecipeForm

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeEditView, self).get_context_data()
        recipe = self.get_object()
        print(recipe.name)
        recipe.categories_list = ""
        categories = Category.objects.filter(recipe=recipe)
        for category in categories:
            if category != categories[categories.__len__() - 1]:
                recipe.categories_list += (category.name + ", ")
            else:
                recipe.categories_list += category.name
        recipe_edit_form = RecipeForm(initial={'recipe_name': recipe.name, 'ingredients_list': recipe.ingredients_list,
                                               'directions': recipe.directions, 'prep_time': recipe.prep_time,
                                               'cook_time': recipe.cook_time, 'servings': recipe.servings,
                                               'source': recipe.source, 'category_input': recipe.categories_list})
        context['recipe'] = recipe
        context['recipe_edit_form'] = recipe_edit_form
        return context

    def post(self, request, **slug):
        if request.method == 'POST':
            search_form = SearchForm(request.POST)
            edit_form = RecipeForm(request.POST)
            if edit_form.is_valid():
                name = edit_form.cleaned_data['recipe_name']
                ingredients_list = edit_form.cleaned_data['ingredients_list']
                directions = edit_form.cleaned_data['directions']
                servings = edit_form.cleaned_data['servings']
                prep_time = edit_form.cleaned_data['prep_time']
                cook_time = edit_form.cleaned_data['cook_time']
                source = edit_form.cleaned_data['source']
                categories = edit_form.cleaned_data['category_input']
                categories_list = []

                if ',' in categories:
                    categories_parsed = categories.split(',')
                    for category in categories_parsed:
                        categories_list.append(category)
                else:
                    categories_list.append(categories)

                recipe = self.update_recipe(name, ingredients_list, directions, servings, prep_time, cook_time, source,
                                            categories_list)
                return redirect('RecipeBook:view_recipe', slug=recipe.slug)
            elif search_form.is_valid():
                name = search_form.cleaned_data['search_name']
                base_url = reverse('RecipeBook:search_results')
                query_string = urlencode({'name': name})
                url = '{}?{}'.format(base_url, query_string)
                return HttpResponseRedirect(url)
            else:
                return render('RecipeBook:edit_recipe', {'form': edit_form})

    def update_recipe(self, name, ingredients_list, directions, servings, prep_time, cook_time, source, categories):
        recipe = self.get_object()
        recipe.name = name
        recipe.ingredients_list = ingredients_list
        recipe.directions = directions
        recipe.servings = servings
        recipe.prep_time = prep_time
        recipe.cook_time = cook_time
        recipe.source = source
        recipe.slug = name + "-" + str(recipe.id)

        while True:
            try:
                recipe.save()
                break
            except db.utils.OperationalError:
                print("DB is locked")
        # clean up categories
        recipe_categories = recipe.categories.all()
        for db_category in recipe_categories:
            recipe.categories.remove(db_category)

        for category in categories:
            try:
                db_category = Category.objects.get(name=category.strip().capitalize())
                recipe.categories.add(db_category)
            except Category.DoesNotExist:
                db_category = self.create_category(category)
                recipe.categories.add(db_category)

        return recipe

    @staticmethod
    def create_category(name):
        while True:
            try:
                db_category = Category.objects.create(name=name.strip().capitalize())
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


class RecipeAddView(BaseFormView):
    model = Recipe
    template_name = 'RecipeBook/add_recipe.html'
    context_object_name = 'recipe_add'
    queryset = None
    form_class = RecipeForm

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeAddView, self).get_context_data()

        context['recipe_add_form'] = RecipeForm(initial={'prep_time': '', 'cook_time': '', 'servings': ''})

        return context

    def post(self, request):
        if request.method == 'POST':
            search_form = SearchForm(request.POST)
            add_form = RecipeForm(request.POST)
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
                print(categories_list)

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
                db_category = Category.objects.get(name=category.strip().capitalize())
                recipe.categories.add(db_category)
            except Category.DoesNotExist:
                db_category = self.create_category(category)
                recipe.categories.add(db_category)

        return recipe

    @staticmethod
    def create_category(name):
        while True:
            try:
                db_category = Category.objects.create(name=name.strip().capitalize())
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
