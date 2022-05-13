# django imports
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    autofocus = True
    search_name = forms.CharField(widget=forms.TextInput(attrs={'size': 30, 'autofocus': autofocus,
                                                                'placeholder': 'Ex: Chicken or Chick',
                                                                'class': 'nav'}),
                                  label='Search by name ',
                                  required=True,
                                  initial='',
                                  )

    def clean_name(self):
        name = self.cleaned_name['search_name']
        return name


class RecipeForm(forms.Form):
    recipe_name = forms.CharField(widget=forms.TextInput(attrs={'size': 110, 'autofocus': True,
                                                                'placeholder': 'Really awesome recipe name'}),
                                  label='Name',
                                  required=True,
                                  initial='')
    ingredients_list = forms.CharField(widget=forms.Textarea(attrs={
        'cols': '100', 'rows': '15', 'placeholder': 'Enter ingredients, one per line'}),
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
    notes = forms.CharField(widget=forms.Textarea(attrs={
        'cols': '100', 'rows': '15', 'placeholder': 'Enter any additional notes here'}),
                            label='Notes',
                            required=False,
                            initial='')
    source = forms.CharField(widget=forms.TextInput(attrs={
        'size': '100', 'placeholder': 'Ex: Family recipe book or www.site.com/recipe'}),
                             label='Source',
                             required=False,
                             initial='')
    category_input = forms.CharField(widget=forms.TextInput(attrs={
        'size': '100', 'placeholder': 'Comma separated list. Ex: Chicken, stew'}),
                                     label='Categories',
                                     required=True,
                                     initial='')


class AccountCreationForm(UserCreationForm, forms.Form):
    """
        Extends the basic UserCreationForm into something that will accept more information for user creation
    """
    error_messages = {
        'username_exists': 'The requested username is already taken'
    }

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'size': '50', 'placeholder': 'Ex: someone@domain.com'}),
        label='E-mail Address',
        required=True,
        initial='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'size': '40'}),
        label='First Name',
        required=True,
        initial='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'size': '40'}),
        label='Last Name',
        required=True,
        initial='')

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name

    def check_username(self):
        username = self.clean_username
        print(username)
        # Check if username already is in the database
        try:
            test_user = User.objects.get(username=username)
            print(test_user)
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists'
            )
        except User.DoesNotExist:
            return True


class RecipeResizingForm(forms.Form):
    """Form to modify ingredients based on desired recipe servings"""
    CHOICES = [(2/1, "Double"), (2/3, "2/3"), (1/2, "1/2"), (1/3, "1/3"), (1/4, "1/4")]
    default_recipe_sizes = forms.ChoiceField(choices=CHOICES,
                                             widget=forms.RadioSelect, label="")
