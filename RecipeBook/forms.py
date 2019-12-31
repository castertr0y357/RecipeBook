# django imports
from django import forms


class SearchForm(forms.Form):
    search_name = forms.CharField(widget=forms.TextInput(attrs={'size': 60}),
                                  label='Search by name: ',
                                  required=True,
                                  initial='',

                                  )

    def clean_name(self):
        name = self.cleaned_name['search_name']

        return name
