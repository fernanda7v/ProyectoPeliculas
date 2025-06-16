from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import requests

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect , get_object_or_404

from django.contrib.auth.decorators import login_required
from .models import Pelicula, Favorito, Genero

def home(request):
    return render(request,'catalogo/home.html')


API_KEY = 'a4f7ad9c1fb770bf24d2e49fe4c826b5'
BASE_URL = "https://api.themoviedb.org/3/discover/movie"

def home2(request):
    genero = request.GET.get("genero", "28")
    pagina = request.GET.get("pagina", "1")

    url = f"{BASE_URL}?api_key={API_KEY}&language=es-ES&sort_by=popularity.desc&page={pagina}&with_genres={genero}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        peliculas = response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        peliculas = []
        print(f"Error en la API de TMDB: {e}")

    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = request.user.favoritos.values_list('pelicula__id', flat=True)

    return render(request, "catalogo/home2.html", {
        "peliculas": peliculas,
        "genero": genero,
        "pagina": pagina,
        "favoritos_ids": favoritos_ids,
    })

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Asegúrate de tener la URL 'login'
    else:
        form = UserCreationForm()
    return render(request, 'catalogo/registro.html', {'form': form})

def agregar_favorito(request, pelicula_id):
    if request.method == "POST":
        # Buscar si ya existe la película
        pelicula = Pelicula.objects.filter(id=pelicula_id).first()

        # Si no existe, obtenemos datos desde TMDB
        if not pelicula:
            url = f"https://api.themoviedb.org/3/movie/{pelicula_id}?api_key={API_KEY}&language=es-ES"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Puedes mejorar esto extrayendo el género correctamente
                genero, _ = Genero.objects.get_or_create(nombre="Sin género")
                pelicula = Pelicula.objects.create(titulo=data['title'], genero=genero)
                # No agregamos actores en este punto

        # Ahora sí, crear favorito si no existe
        Favorito.objects.get_or_create(usuario=request.user, pelicula=pelicula)

    return redirect('home2')