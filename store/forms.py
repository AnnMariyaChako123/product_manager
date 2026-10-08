from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            "name",
            "sku",
            "category",
            "price",
            "stock",
            "image",
            "description",
            "status",
        ]

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price <= 0:
            raise forms.ValidationError(
                "Price must be greater than 0."
            )

        return price

    def clean_stock(self):
        stock = self.cleaned_data["stock"]

        if stock < 0:
            raise forms.ValidationError(
                "Stock cannot be negative."
            )

        return stock