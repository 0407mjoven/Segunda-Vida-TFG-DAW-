from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Perfil(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField(blank =True, null=True)
    biografía = models.TextField(blank = True, null = True)
    localizacion = models.CharField(blank = True, null = True, max_length=1000)
    foto = models.ImageField(upload_to="perfil", default='perfil/blankprofile.webp')
    create_datetime = models.DateTimeField(auto_now_add= True)
    customer_id = models.CharField(blank=True,null=True,max_length = 100)

    def seguidores(self):
        return self.seguidor.all().count()
    
    def seguidos(self):
        return self.seguido.all().count()
    
    def productos_asociados(self):
        return self.productos.all()
    
    def __str__(self) -> str:
        return self.username
class Categoria(models.Model):
    
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length = 1000)
    icono = models.CharField(max_length=1000)
    
    def __str__(self) -> str:
        return self.nombre
    
class Producto(models.Model):
    
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length = 100, null = True)
    descripcion = models.TextField(max_length=500)
    precio = models.FloatField()
    imagen = models.ImageField(upload_to="productos/", blank=True)
    imagen2 = models.ImageField(upload_to="productos/", blank=True)
    imagen3 = models.ImageField(upload_to="productos/" ,blank=True)
    user_id = models.ForeignKey(Perfil,related_name='productos', on_delete=models.CASCADE)
    categorias = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(auto_now_add = True)
    product_id = models.CharField(blank=True,null=True,max_length = 100)
    price_id = models.CharField(blank=True,null=True,max_length = 100)
    
    def recientes():
        return Producto.objects.all().order_by('create_datetime')
    
    
    
class Comentario(models.Model):
    
    texto = models.TextField(blank=True,null=True)
    emisor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name = 'emisor')
    receptor = models.ForeignKey(Perfil, on_delete=models.CASCADE,  related_name = 'receptor')
    create_datetime = models.DateTimeField(auto_now_add = True)


class Seguidor(models.Model):
    
    seguidor = models.ForeignKey(Perfil,on_delete=models.CASCADE, related_name = 'seguidor')
    seguido = models.ForeignKey(Perfil,on_delete=models.CASCADE, related_name = 'seguido')
