from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductoListView.as_view(), name='index'),
    path('accounts/login',LoginView.as_view(), name='login'),
    path('accounts/logout',LogoutView.as_view(), name='logout'),
    path('accounts/register',LogoutView.as_view(), name='logout'),
    path('product/<pk>',ProductoDetailView.as_view(), name='producto_detail'),
    path('product_create/', ProductoUploadView.as_view(), name='product_create')

]