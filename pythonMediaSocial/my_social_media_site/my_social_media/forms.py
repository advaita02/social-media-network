from django import forms


class YearForm(forms.Form):
    year_choices = [(year, year) for year in range(2000, 2030)]
    year = forms.ChoiceField(choices=year_choices)
