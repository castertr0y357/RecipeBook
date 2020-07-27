# django imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    search_name = forms.CharField(widget=forms.TextInput(attrs={'size': 30, 'autofocus': True,
                                                                'placeholder': 'Ex: Chicken or Chick'}),
                                  label='Search by name ',
                                  required=True,
                                  initial='',
                                  )

    def clean_name(self):
        name = self.cleaned_name['search_name']

        return name


class RecipeForm(forms.Form):
    recipe_name = forms.CharField(widget=forms.TextInput(attrs={
        'size': 110, 'placeholder': 'Really awesome recipe name'}),
                                  label='Name',
                                  required=True,
                                  initial='')
    ingredients_list = forms.CharField(widget=forms.Textarea(attrs={
        'cols': '50', 'rows': '15', 'placeholder': 'Enter ingredients, one per line'}),
                                       label='Ingredients',
                                       required=True,
                                       initial='')
    directions = forms.CharField(widget=forms.Textarea(attrs={
        'cols': '100', 'rows': '15', 'placeholder': 'Enter directions here'}),
                                 label='Directions',
                                 required=True,
                                 initial='')
    prep_time = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter time in minutes'}),
                                   label='Prep Time',
                                   required=False,
                                   initial='')
    cook_time = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter time in minutes'}),
                                   label='Cook Time',
                                   required=True,
                                   initial='')
    servings = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Ex: 4 or 6'}),
                                  label='# of Servings',
                                  required=True,
                                  initial='')
    source = forms.CharField(widget=forms.TextInput(attrs={
        'size': '40', 'placeholder': 'Ex: Family recipe book or www.site.com/recipe'}),
                             label='Source',
                             required=False,
                             initial='')
    category_input = forms.CharField(widget=forms.TextInput(attrs={
        'size': '40', 'placeholder': 'Comma separated list. Ex: Chicken, stew'}),
                                     label='Categories',
                                     required=True,
                                     initial='')


class AccountCreationForm(UserCreationForm, forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'size': '50', 'placeholder': 'Ex: someone@domain.com'}),
        label='E-mail Address',
        required=True,
        initial='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'size': '20', 'placeholder': 'First Name'}),
        label='First Name',
        required=True,
        initial='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'size': '40', 'placeholder': 'Last Name'}),
        label='Last Name',
        required=True,
        initial='')
