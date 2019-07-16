from django.views import generic
from .models import Category, Recipe


class MainView(generic.ListView):
    model = Category
    template_name = 'RecipeBook/main_page.html'
    context_object_name = 'categories'
    queryset = Category.objects.all().order_by('category_name')


class CategoryView(generic.DetailView):
    model = Category
    context_object_name = 'category_recipe_list'
    queryset = None
    slug_field = 'category_name'
    slug_url_kwarg = 'category_name'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryView, self).get_context_data()
        category = self.object

        recipes = Recipe.objects.filter(category=category)

        context['recipes'] = recipes

        return context


