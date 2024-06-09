from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView,FormView, View, TemplateView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LogoutView
from .forms import *
import stripe

stripe.api_key = "sk_test_51PKHA2KAZUWMcIwofIABfOT9YZfEfWIBl9Fa2pr2cV56AkCro7uWXFzdMAIJc7LaSql8ApwvFOEQv8PLXnc0JJKV00hHR10wgv"
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
            context['verano'] = Categoria.objects.filter(nombre__in = ['Deportes','Libros','Coleccionismo','Juegos','Instrumentos','Smartwatchs'] )
            return context

class ProductoListView(LoginRequiredMixin, TemplateView):
    template_name = 'producto_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria = Categoria.objects.get(id=self.kwargs['pk'])
        context['productos'] = Producto.objects.filter(categorias=categoria)
        context['perfil'] = Perfil.objects.get(user_id=self.request.user.id)
        context['categorias'] = Categoria.objects.all()
        context['object'] = categoria
        context['form_busqueda'] = FormularioBusqueda()  # Cambié el nombre del contexto para evitar conflictos
        context['ciudades'] = PROVINCIAS_CHOICES_ARRAY
        return context

    def post(self, request, *args, **kwargs):
        categoria = Categoria.objects.get(id=self.kwargs['pk'])
        productos = Producto.objects.filter(categorias=categoria)
        form = FormularioBusqueda(request.POST)
        
        if form.is_valid():
            precio_minimo = form.cleaned_data.get('precio_minimo')
            precio_maximo = form.cleaned_data.get('precio_maximo')
            print(form.cleaned_data)
            print(precio_minimo,precio_maximo)
            if precio_minimo is not None:
                productos = productos.filter(precio__gte=precio_minimo)
            if precio_maximo is not None:
                productos = productos.filter(precio__lte=precio_maximo)
            print(productos)
        context = {
            'productos': productos,
            'form': form,
            'perfil': Perfil.objects.get(user_id=self.request.user.id),
            'categorias': Categoria.objects.all(),
            'object': categoria,
            'form_busqueda': FormularioBusqueda(),
            'ciudades': PROVINCIAS_CHOICES_ARRAY
        }
        return render(request, 'producto_list.html', context)

class BuscarProducto(LoginRequiredMixin,TemplateView):
    
    template_name = 'product_search.html'
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.method == 'GET' and 'keyword' in self.request.GET:
            
            term = self.request.GET.get('keyword')
            resultados = Producto.objects.filter(nombre__icontains=term)
        context = super().get_context_data(**kwargs)
        context['productos'] = resultados
        context['perfil'] = Perfil.objects.get(user_id = self.request.user.id)
        context['categorias'] = Categoria.objects.all()
        context['busqueda'] = True
        context['form'] = FormularioBusqueda
        context['numero'] = len(resultados)
        context['ciudades'] = PROVINCIAS_CHOICES_ARRAY

        return context
    
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
        contexto['perfil'] = Perfil.objects.get(user_id = self.request.user.id)
        
        return contexto
    

class ProductoCreateView(LoginRequiredMixin, CreateView):
    
    model = Producto
    template_name = 'producto_form.html'
    form_class = ProductoForm
    success_url = '/'
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = ProductoForm(self.request.POST,  self.request.FILES)
        form.instance.user_id = Perfil.objects.get(user = self.request.user.pk)
        if form.is_valid():
            objeto = form.save(commit=False)
            producto = stripe.Product.create(name=form.cleaned_data['nombre'],description=form.cleaned_data['descripcion'],id=objeto.pk)
            precius = int(form.cleaned_data['precio'])
            precio = stripe.Price.create(
            product=producto.id,
            unit_amount= precius * 100,  # El precio en centavos (por ejemplo, 2000 centavos = 20.00 USD)
            currency='eur',
            )
            objeto.product_id = producto.id
            objeto.price_id = precio.id
            objeto.save()
        else:
            form = ProductoForm()
            return render(request, 'producto_form.html', {'form': form})

        return redirect('index')
    
    
class PerfilDetailView(DetailView):
    
    model= Perfil
    template_name = 'perfil.html'
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            print(self.kwargs)
            context = self.get_context_data()
            print(context)
            return self.render_to_response(context)
        else:
            return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['perfil'] = Perfil.objects.get(user_id = self.request.user.id)
        contexto['perfil2'] = Perfil.objects.get(user_id = self.kwargs['pk'])
        contexto['form'] = CommentForm()
        contexto['comentarios'] = Comentario.objects.filter(receptor = contexto['perfil2'] )
        contexto['sigue'] = Seguidor.objects.filter(seguidor= Perfil.objects.get(user =self.request.user.pk),seguido=Perfil.objects.get(user = User.objects.get(id = self.kwargs['pk'])))
        return contexto
    
    
def comentar(request, *args, **kwargs):
    form = CommentForm(request.POST)
    if form.is_valid():
        comentario = form.cleaned_data['comentario']
        Comentario.objects.create(texto = comentario, emisor = Perfil.objects.get(user =request.user.pk), receptor =Perfil.objects.get(pk = kwargs['pk']))
    return redirect ('../perfil/'+kwargs['pk'])
        

class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = Perfil
    template_name = 'perfil_update.html'
    success_url = '/'
    form_class = ProfileUpdate

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #    context = super().get_context_data(**kwargs)
    #    context["form"] = self.form_class(instance=self.get_object())
    #    return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        perfil = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.instance.user = User.objects.get(id=self.request.user.id)
            producto = form.save()
            perfil = Perfil.objects.get(user_id=self.request.user.id)
            print(perfil.biografía)
            return redirect('../perfil/'+str(self.request.user.id))
        else:
            return self.form_invalid(form)
        
def logout_view(request):
        logout(request)
        return redirect("/")
    
class RegisterUserView(FormView):
    
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    
    def post(self, request):
         if request.method == "POST":
            form = RegisterUserForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                user = form.save()
                if form.cleaned_data.get('foto_perfil', None) == None:
                    Perfil.objects.create(
                        user=user,
                        fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                        biografía=form.cleaned_data.get('biografia', ''),
                        username = form.cleaned_data['username'],
                    
                        localizacion = form.cleaned_data['localizacion']
                    )
                else:
                        Perfil.objects.create(
                        user=user,
                        username = form.cleaned_data['username'],
                        fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                        biografía=form.cleaned_data.get('biografia', ''),
                        foto=form.cleaned_data.get('foto_perfil', None),
                      
                        localizacion = form.cleaned_data['localizacion']
                    )
                        
                print(form.cleaned_data.get('foto_perfil', None))        
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
            else:
                return render(request, 'registration/register.html', {'form': form})
                

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    template_name = 'producto_update.html'
    success_url = '/'
    form_class = ProductoForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs) -> dict[str, Any]:
    #    context = super().get_context_data(**kwargs)
    #    context["form"] = self.form_class(instance=self.get_object())
    #    return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        producto = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=producto)
        print(form)
        if form.is_valid():
            form.instance.user_id = Perfil.objects.get(user_id=self.request.user.id)
            producto = form.save()
            perfil = Perfil.objects.get(user_id=self.request.user.id)
            return redirect('../perfil/'+str(self.request.user.id))
        else:
            return self.form_invalid(form)
        
        
class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto_delete.html'
    success_url = '/'

    
def seguir(request, *args, **kwargs):
    Seguidor.objects.create(seguidor = Perfil.objects.get(user = request.user.pk), seguido = Perfil.objects.get(user = kwargs['pk']) )
    return redirect('../perfil/'+str(kwargs['pk']))
        
class Compra(View):
    template_name = 'compra.html'
    
    def get(self, request, *args, **kwargs):
        producto = get_object_or_404(Producto, pk=self.kwargs['pk'])
        imagenes = [producto.imagen] if isinstance(producto.imagen, str) else producto.imagen
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {
                            "name": producto.nombre,
                            "description": producto.descripcion,
                        },
                        "unit_amount": int(producto.precio * 100),  # convertir a centavos
                    },
                    "quantity": 1,
                    
                }
                
            ],
            
            mode="payment",
            success_url=request.build_absolute_uri('/') + 'success/'+self.kwargs['pk'],
            cancel_url=request.build_absolute_uri('/') + 'producto_detail/'+self.kwargs['pk'],
        )
        return redirect(checkout_session.url, code=303)
    
def exito(request,*args, **kwargs):
    producto = Producto.objects.get(id = kwargs['pk'])
    producto.delete()
    return render(request,'compra.html',)