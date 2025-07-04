from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Actor(models.Model):
    nombre=models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
    
class Genero(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Pelicula(models.Model):
    titulo=models.CharField(max_length=100)
    genero=models.ForeignKey('Genero',on_delete=models.CASCADE)
    actores=models.ManyToManyField(Actor)
    favoritos = models.ManyToManyField(User, related_name='peliculas_favoritas', blank=True)

    def __str__(self):
        return self.titulo
    def promedio_de_valoraciones(self):
        valoraciones = self.valoraciones.all()
        if valoraciones.exists():
            total = sum([v.puntuacion for v in valoraciones])
            return total / valoraciones.count()
        return 0

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='favorita_de')

    class Meta:
        unique_together = ('usuario', 'pelicula')  # Evita duplicados

    def __str__(self):
        return f"{self.usuario.username} - {self.pelicula.titulo}"

class Valoracion(models.Model):
    pelicula=models.ForeignKey('Pelicula',on_delete=models.CASCADE,related_name='valoraciones')
    puntuacion=models.IntegerField()
    comentario=models.TextField(blank=True)

    def __str__(self):
        return f"{self.pelicula.titulo}-{self.puntuacion}/5"