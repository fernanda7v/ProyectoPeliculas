from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
# Create your views here.

#from django.http import HttpResponse

#def index(request):
#    return HttpResponse("¡Bienvenido al Catálogo de Películas!")
def home(request):
    return render(request,'catalogo/home.html')
