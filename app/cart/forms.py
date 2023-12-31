from django import forms

QUANTITY_CHOICES = ([(i, str(i)) for i in range (1, 6)])


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
