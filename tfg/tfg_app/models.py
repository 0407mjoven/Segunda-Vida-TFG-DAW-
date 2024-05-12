from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Perfil(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    edad = models.IntegerField(blank =True, null=True)
    localizacion = models.CharField(blank = True, null = True, max_length=1000)
    foto = models.ImageField(upload_to="perfil")
    
    def comentariosRecibidos(self):
        return self.comentario_set.all()
    
    def productosSubidos(self):
        return self.producto_set.all()
    
    def seguidores(self):
        return  Comentario.objects.filter(seguido = self.pk).count()
    
    def seguidos(self):
        return  Comentario.objects.filter(seguido = self.pk).count()
class Categoria(models.Model):
    
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length = 1000)
    
class Producto(models.Model):
    
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length = 100, null = True)
    descripcion = models.TextField(max_length=500)
    precio = models.FloatField()
    imagen = models.ImageField(upload_to="productos")
    imagen2 = models.ImageField(upload_to="productos", blank=True)
    imagen3 = models.ImageField(upload_to="productos" ,blank=True)
    user_id = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria, blank=True)
    
   
class Comentario(models.Model):
    
    texto = models.TextField(blank=True,null=True)
    emisor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name = 'emisor')
    receptor = models.ForeignKey(Perfil, on_delete=models.CASCADE,  related_name = 'receptor')


class Seguidor(models.Model):
    
    seguidor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name = 'seguidor')
    seguido = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name = 'seguido')
