from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name="shop"),
    path('create_order/', views.takes_order, name="order"),
    path('create_customer/', views.create_customer, name="create_customer"),
    path('manage_order/<str:pk>', views.manage_order, name="manage_order"),
    path('cart/<str:pk>', views.cart, name="cart"),
    path('checkout/<str:pk>', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('invoice/<str:pk>', views.DownloadPDF.as_view(), name="invoice"),
    path('process_order/', views.process_order, name="process_order"),
]
