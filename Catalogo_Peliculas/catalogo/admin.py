from django.contrib import admin
from .models import Actor, Genero, Pelicula, Valoracion
# Register your models here.
admin.site.register(Actor)
admin.site.register(Genero)
admin.site.register(Pelicula)
admin.site.register(Valoracion)