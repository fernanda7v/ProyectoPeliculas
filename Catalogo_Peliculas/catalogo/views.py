from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
import requests

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


def home(request):
    return render(request,'catalogo/home.html')


API_KEY = 'a4f7ad9c1fb770bf24d2e49fe4c826b5'
BASE_URL = "https://api.themoviedb.org/3/discover/movie"

def home2(request):
    genero = request.GET.get("genero", "28")  # Acción por defecto
    pagina = request.GET.get("pagina", "1")  # Página 1 por defecto

    url = f"{BASE_URL}?api_key={API_KEY}&language=es-ES&sort_by=popularity.desc&page={pagina}&with_genres={genero}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        peliculas = response.json().get("results", [])

        print(f"Películas obtenidas: {peliculas}")  # Verifica si hay datos
    except requests.exceptions.RequestException as e:
        peliculas = []
        print(f"Error en la API de TMDB: {e}")

    return render(request, "catalogo/home2.html", {"peliculas": peliculas, "genero": genero, "pagina": pagina})

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Asegúrate de tener la URL 'login'
    else:
        form = UserCreationForm()
    return render(request, 'catalogo/registro.html', {'form': form})