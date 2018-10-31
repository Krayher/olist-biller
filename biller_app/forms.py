from django import forms


class BillerForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    subscriber = forms.IntegerField(label='Subscriber', min_value=1, max_value=99999999999, required=True)
    month = forms.IntegerField(label='Month', max_value=12, min_value=1, required=False)
    year = forms.IntegerField(label='Year', min_value=1900, max_value=2099, required=False)
