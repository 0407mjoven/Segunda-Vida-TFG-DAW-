from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import *

urlpatterns = [
    path('', Menu.as_view(), name='index'),
    path('product_list/<pk>', ProductoListView.as_view(), name='product_list'),
    path('buscar_producto/', BuscarProducto.as_view(), name='buscar_producto'),
    path('accounts/register',RegisterUserView.as_view(), name= 'register'),
    path('logout/',logout_view, name= 'logout'),
    path('product/<pk>',ProductoDetailView.as_view(), name='product_detail'),
    path('product_create/', ProductoCreateView.as_view(), name='product_create'),
    path('perfil/<pk>', PerfilDetailView.as_view(), name='perfil'),
    path('perfil_update/<pk>', PerfilUpdateView.as_view(), name='perfil_update'),
    path('product_update/<pk>',ProductoUpdateView.as_view(), name='product_update'),
    path('producto/<int:pk>/eliminar/', ProductoDeleteView.as_view(), name='product_delete'),
    path('compra/<pk>', Compra.as_view(), name='compra'),
    path('seguir/<pk>',seguir, name='seguir'),
    path('success/<pk>',exito, name='success'),
    path('comentar/<pk>',comentar, name='comentar'),
    
    
    



]