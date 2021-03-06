from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class Customer(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.CharField(max_length=200, null=True, blank=True)
    cell_no = models.CharField(max_length=200, unique=True, null=False, blank=False)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    days = models.IntegerField(default=1, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def transaction_id(self):
        t_id = str("LMS_" + str(self.id + 1000))
        return t_id

    @property
    def deliver_date(self):

        orderitems = self.orderitem_set.all()
        days = max([item.day for item in orderitems])
        x = self.date_ordered + timedelta(days)
        dd = x.strftime("%b. %d, %Y")

        return dd

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    @property
    def day(self):
        return self.product.days
