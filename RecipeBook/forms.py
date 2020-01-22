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


class RecipeForm(forms.Form):
    recipe_name = forms.CharField(widget=forms.TextInput(attrs={'size': 110}),
                                  label='Name',
                                  required=True,
                                  initial='')
    ingredients_list = forms.CharField(widget=forms.Textarea(attrs={'cols': '50', 'rows': '15'}),
                                       label='Ingredients',
                                       required=True,
                                       initial='')
    directions = forms.CharField(widget=forms.Textarea(attrs={'cols': '100', 'rows': '15'}),
                                 label='Directions',
                                 required=True,
                                 initial='')
    prep_time = forms.IntegerField(widget=forms.NumberInput,
                                   label='Prep Time',
                                   required=False,
                                   initial='')
    cook_time = forms.IntegerField(widget=forms.NumberInput,
                                   label='Cook Time',
                                   required=True,
                                   initial='')
    servings = forms.IntegerField(widget=forms.NumberInput,
                                  label='# of Servings',
                                  required=True,
                                  initial='')
    source = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}),
                             label='Source',
                             required=False,
                             initial='')
    category_input = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}),
                                     label='Categories',
                                     required=True,
                                     initial='')
