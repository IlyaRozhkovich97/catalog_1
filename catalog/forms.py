from django import forms
from django.forms import ModelForm, ValidationError, BooleanField
from .models import Product


class StyleFormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'purchase_price', 'image']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман',
                           'полиция', 'радар']
        for word in forbidden_words:
            if word in name:
                raise forms.ValidationError(f"Запрещенное слово '{word}' в названии")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                           'обман', 'полиция', 'радар']
        for word in forbidden_words:
            if word in description:
                raise forms.ValidationError(f"Запрещенное слово '{word}' в описании")
        return description
