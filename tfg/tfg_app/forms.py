
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
PROVINCIAS_CHOICES = [
    ('A Coruña', 'A Coruña'),
    ('Álava', 'Álava'),
    ('Albacete', 'Albacete'),
    ('Alicante', 'Alicante'),
    ('Almería', 'Almería'),
    ('Asturias', 'Asturias'),
    ('Ávila', 'Ávila'),
    ('Badajoz', 'Badajoz'),
    ('Baleares', 'Baleares'),
    ('Barcelona', 'Barcelona'),
    ('Burgos', 'Burgos'),
    ('Cáceres', 'Cáceres'),
    ('Cádiz', 'Cádiz'),
    ('Cantabria', 'Cantabria'),
    ('Castellón', 'Castellón'),
    ('Ciudad Real', 'Ciudad Real'),
    ('Córdoba', 'Córdoba'),
    ('Cuenca', 'Cuenca'),
    ('Girona', 'Girona'),
    ('Granada', 'Granada'),
    ('Guadalajara', 'Guadalajara'),
    ('Guipúzcoa', 'Guipúzcoa'),
    ('Huelva', 'Huelva'),
    ('Huesca', 'Huesca'),
    ('Jaén', 'Jaén'),
    ('La Rioja', 'La Rioja'),
    ('Las Palmas', 'Las Palmas'),
    ('León', 'León'),
    ('Lleida', 'Lleida'),
    ('Lugo', 'Lugo'),
    ('Madrid', 'Madrid'),
    ('Málaga', 'Málaga'),
    ('Murcia', 'Murcia'),
    ('Navarra', 'Navarra'),
    ('Ourense', 'Ourense'),
    ('Palencia', 'Palencia'),
    ('Pontevedra', 'Pontevedra'),
    ('Salamanca', 'Salamanca'),
    ('Segovia', 'Segovia'),
    ('Sevilla', 'Sevilla'),
    ('Soria', 'Soria'),
    ('Tarragona', 'Tarragona'),
    ('Santa Cruz de Tenerife', 'Santa Cruz de Tenerife'),
    ('Teruel', 'Teruel'),
    ('Toledo', 'Toledo'),
    ('Valencia', 'Valencia'),
    ('Valladolid', 'Valladolid'),
    ('Vizcaya', 'Vizcaya'),
    ('Zamora', 'Zamora'),
    ('Zaragoza', 'Zaragoza'),
]

# forms.py

PROVINCIAS_CHOICES_ARRAY = [
    'A Coruña', 'Álava', 'Albacete', 'Alicante', 'Almería', 'Asturias', 'Ávila', 
    'Badajoz', 'Baleares', 'Barcelona', 'Burgos', 'Cáceres', 'Cádiz', 'Cantabria', 
    'Castellón', 'Ciudad Real', 'Córdoba', 'Cuenca', 'Girona', 'Granada', 'Guadalajara', 
    'Guipúzcoa', 'Huelva', 'Huesca', 'Jaén', 'La Rioja', 'Las Palmas', 'León', 
    'Lleida', 'Lugo', 'Madrid', 'Málaga', 'Murcia', 'Navarra', 'Ourense', 'Palencia', 
    'Pontevedra', 'Salamanca', 'Segovia', 'Sevilla', 'Soria', 'Tarragona', 'Santa Cruz de Tenerife', 
    'Teruel', 'Toledo', 'Valencia', 'Valladolid', 'Vizcaya', 'Zamora', 'Zaragoza'
]

nombres = {}
for categoria in Categoria.objects.all():
        nombres[categoria.nombre] = categoria.nombre
        
        
class FiltroProductoForm(forms.Form):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(),required=False,widget=forms.RadioSelect)
    
class CommentForm(forms.Form):
    comentario = forms.CharField()
    
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'class': 'form-control'})
    )
    first_name = forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'})
    )
    last_name = forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'form-control'})
    )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'class': 'form-control'}))
    biografia = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Biografía', 'class': 'form-control'}),required=False)
    foto_perfil = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha de nacimiento', 'class': 'form-control'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}),required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña', 'class': 'form-control'}),required=True)
    localizacion = forms.ChoiceField(label='Provincia', choices=PROVINCIAS_CHOICES, required=False,widget=forms.Select(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'fecha_nacimiento', 'password1','password2']
    
class FormularioBusqueda(forms.Form):
    precio_minimo = forms.DecimalField(label='Precio mínimo', required=False, min_value=0, decimal_places=2)
    precio_maximo = forms.DecimalField(label='Precio máximo', required=False, min_value=0, decimal_places=2)
    provincia = forms.CharField(label='Provincia', required=False)
    
class ProductoForm(forms.ModelForm):
    
    nombre = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))
    precio = forms.CharField(widget=forms.NumberInput(attrs={ 'class': 'form-control'}))
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    imagen2 = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control'}))
    imagen3 = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control'}))
    categorias = forms.ModelChoiceField(queryset=Categoria.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),required=False)
    
    class Meta:
        model = Producto
        fields = ("nombre", 'precio', 'imagen', 'imagen2', 'imagen3', 'categorias', 'descripcion')

    categorias = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        widget=forms.Select
    )

class ProfileUpdate(forms.ModelForm):
    
    username = forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'})
    )
    biografía = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Biografía', 'class': 'form-control'}),required=False)
    foto_perfil = forms.ImageField(required=False,widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Fecha de nacimiento', 'class': 'form-control'}), required=True)
    localizacion = forms.ChoiceField(label='Provincia', choices=PROVINCIAS_CHOICES, required=False,widget=forms.Select(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}))
    
    class Meta:
        model = Perfil
        fields = ('username','fecha_nacimiento','foto_perfil','biografía','localizacion')