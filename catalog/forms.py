from .models import Item, Fabric, Supplier, Customer, Receipt
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from datetime import datetime
import datetime as dt
from django import forms
import pytz


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and (price < 1 or price > 5000):
            raise ValidationError('Неправильна ціна, можливий діапазон від 1 до 5000')
        return round(price, 2)
