from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView,FormView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

class ProductoListView(ListView):
    
    model = Producto
    template_name = 'producto_list.html'
    context_object_name = 'productos'
    
    def get_context_data(self, **kwargs: Any):
        contexto = super().get_context_data(**kwargs)
        contexto['productos'] = Producto.objects.all()
        contexto['categorias'] = Categoria.objects.all()
        return contexto
        
class ProductoDetailView(LoginRequiredMixin,DetailView):
    
    model = Producto
    template_name = 'producto_list.html'
    
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = self.get_context_data(request)
            return self.render_to_response(context)
        else:
            return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['producto'] = self.get_object()
        return contexto
    
class ProductoUploadView(LoginRequiredMixin, CreateView):
    
    model = Producto
    template_name = 'producto_form.html'
    fields = '__all__'
    success_url = '/'
    
   
    def form_valid(self, form):
        # Procesar el formulario aquí
        # Puedes acceder a los datos del formulario a través de 'form.cleaned_data'
        return super().form_valid(form)
    
class PerfilView(DetailView):
    
    model= Perfil
    template_name = 'perfil.html'
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = self.get_context_data(request)
            return self.render_to_response(context)
        else:
            return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['perfil'] = Perfil.objects.get(user_id = self.request.user.id)
        return contexto