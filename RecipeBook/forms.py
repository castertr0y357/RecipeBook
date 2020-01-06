# django imports
from django import forms
from .models import Recipe


class SearchForm(forms.Form):
    search_name = forms.CharField(widget=forms.TextInput(attrs={'size': 60}),
                                  label='Search by name ',
                                  required=True,
                                  initial='',
                                  )

    def clean_name(self):
        name = self.cleaned_name['search_name']

        return name


class RecipeAddForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients_list', 'directions', 'prep_time', 'cook_time', 'servings', 'url', 'categories']
        widgets = {
            'name': forms.TextInput(attrs={'size': '110'}),
            'ingredients_list': forms.Textarea(attrs={'cols': '50', 'rows': '15'}),
            'directions': forms.Textarea(attrs={'cols': '100', 'rows': '15'}),
            'url': forms.URLInput(attrs={'size': '100'}),
            'categories': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'ingredients_list': 'Ingredients'
        }
        error_messages = {
            'name': {
                'max_length': "The recipe name is too long.",
                'null': "The recipe has to have a name",
            },

        }
