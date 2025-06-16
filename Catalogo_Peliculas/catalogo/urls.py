from django.urls import path
from . import views

urlpatterns = [
    path('favorito/<int:pelicula_id>/', views.agregar_favorito, name='agregar_favorito'),
    path('', views.home2, name='home2'),  
    path('registro/', views.registrar_usuario, name='registro'),
]
