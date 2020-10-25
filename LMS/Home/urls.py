from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin_home/', views.admin_home, name="admin_home"),
    path('staff_home/', views.staff_home, name="staff_home"),
    path('register/', views.registerpage, name="register"),
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutpage, name="logout"),
]
