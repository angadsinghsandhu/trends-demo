from django import forms
 
# creating a form
class TrendForm(forms.Form):
    model_type = forms.ChoiceField(choices=[('nyt', "New York Times Data")])
    base_term = forms.CharField(max_length = 200)
    rel_term1 = forms.CharField(max_length = 200)
    rel_term2 = forms.CharField(max_length = 200)
    rel_term3 = forms.CharField(max_length = 200)
    rel_term4 = forms.CharField(max_length = 200)