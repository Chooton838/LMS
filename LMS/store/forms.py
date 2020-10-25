from django.forms import ModelForm
from .models import Product, Customer, OrderItem, Order


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
