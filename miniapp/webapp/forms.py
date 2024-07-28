from django import forms


class BuyGoldForm(forms.Form):
    amount = forms.IntegerField(min_value=1)


class SellGoldForm(forms.Form):
    amount = forms.IntegerField(min_value=1)
