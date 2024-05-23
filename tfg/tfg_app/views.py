from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView,FormView, View, TemplateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from .forms import *

class Login(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '../'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect ('/')
class Menu(LoginRequiredMixin,TemplateView):
    
    template_name = 'menu.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['perfil'] = Perfil.objects.get(user_id = self.request.user.id)
            context['informaticos'] = Categoria.objects.filter(nombre__in = ['Consolas','Auriculares','Teléfonos','Ordenadores','Videojuegos','Smartwatchs'] )
            context['verano'] = Categoria.objects.filter(nombre__in = ['Deportes','Libros','Teléfonos','Ordenadores','Videojuegos','Smartwatchs'] )
            return context

class ProductoListView(LoginRequiredMixin, TemplateView):
    template_name = 'menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()
        context['form'] = FiltroProductoForm
        context['perfil'] = Perfil.objects.get(user_id = self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        form = FiltroProductoForm(request.POST)
        if form.is_valid():
            categoria_seleccionada = form.cleaned_data['categoria']
            if categoria_seleccionada == '-----------':
                productos_filtrados = Producto.objects.all()
            else:
                productos_filtrados = Producto.objects.filter(categorias=Categoria.objects.get(nombre=categoria_seleccionada))
                
            return render(request, self.template_name, {'form': form, 'productos': productos_filtrados, 'perfil' : Perfil.objects.get(user_id = self.request.user.id)})
        else:
            return render(request, self.template_name, {'form': form,  'perfil' : Perfil.objects.get(user_id = self.request.user.id)})
        
class ProductoDetailView(LoginRequiredMixin,DetailView):
    
    model = Producto
    template_name = 'producto_detail.html'
    
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = self.get_context_data()
            return self.render_to_response(context)
        else:
            return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        contexto  ={} 
        contexto['producto'] = self.get_object()
        return contexto
    
class ProductoCreateView(LoginRequiredMixin, CreateView):
    
    model = Producto
    template_name = 'producto_form.html'
    form_class = ProductoForm
    success_url = '/'
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = ProductoForm(request.POST,  request.FILES)
        form.instance.user_id = Perfil.objects.get(user = self.request.user.pk)
        if form.is_valid():
            return super().form_valid(form)
    
    
class PerfilDetailView(DetailView):
    
    model= Perfil
    template_name = 'perfil.html'
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = self.get_context_data()
            return self.render_to_response(context)
        else:
            return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['perfil'] = Perfil.objects.get(user_id = self.kwargs['pk'])
        contexto['form'] = CommentForm()
        contexto['comentarios'] = Comentario.objects.filter(receptor = contexto['perfil'] )
        return contexto
    
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.cleaned_data['comentario']
            Comentario.objects.create(texto = comentario, emisor = Perfil.objects.get(user =self.request.user.pk), receptor =Perfil.objects.get(user = self.kwargs['pk']))
        return redirect ('../perfil/'+self.kwargs['pk'])
        
 
def logout_view(request):
        logout(request)
        return redirect("/")
    
class RegisterUserView(FormView):
    
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    
    def post(self, request):
         if request.method == "POST":
            form = RegisterUserForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                Perfil.objects.create(
                    user=user,
                    fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                    biografía=form.cleaned_data.get('biografia', ''),
                    foto=form.cleaned_data.get('foto_perfil', None),
                    localizacion = 'Zaragoza'
                )
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Producto
    template_name = 'producto_update.html'
    success_url = '/'
    form_class = ProductoForm
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
   
    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #    context ={}
    #    context["form"] = ProductoForm()
    #    context["object"] = self.get_object()
    #    return context
   
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.method == 'POST':
            form = ProductoForm(request.POST, request.FILES)
            producto = Producto.objects.get(id = self.kwargs['pk'])

            if form.is_valid():
                form.instance.user_id = Perfil.objects.get(user_id = producto.user_id.user)
                producto = form.save()
                categorias = form.cleaned_data['categorias']
                perfil = Perfil.objects.get(user_id = producto.user_id.user)
                return redirect('../perfil/'+str(perfil.pk))
            else:
                return redirect('register')
        
        
class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto_delete.html'
    success_url = '/'

class Seguir(CreateView):
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        Seguidor.objects.create(seguidor = Perfil.objects.get(user = self.request.user.pk), seguido = Perfil.objects.get(user = self.kwargs['pk']) )
        return super().post(request, *args, **kwargs)