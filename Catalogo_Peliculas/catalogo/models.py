from django.db import models

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
    genero=models.ForeignKey('Genero',on_delete=models.CASCADE)#on_delete es para borrar un genero y tambien hace referencia ala clase Genero creada
    actores=models.ManyToManyField(Actor)#ManyTooManyfield el actor puede estar en una o muchas peliculas o tener una pelicula muchos actores

    def __str__(self):
        return self.titulo
    def promedio_de_valoraciones(self):
        valoraciones=self.valoraciones.all()
        if valoraciones.exists():
            total=0
            for x in valoraciones:
                total+=x.puntuacion
            return total/valoraciones.count()
        else:
            return 0
class Valoracion(models.Model):
    pelicula=models.ForeignKey('Pelicula',on_delete=models.CASCADE,related_name='valoraciones')
    puntuacion=models.IntegerField()
    comentario=models.TextField(blank=True)

    def __str__(self):
        return f"{self.pelicula.titulo}-{self.puntuacion}/5"