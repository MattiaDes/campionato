from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from squadre.models import Calendario

# Pagina principale del sito
def home(request):
    title = Calendario.objects.values('nomeCampionato').distinct().first()
    return render(request, 'squadre/home.html', {'title': title})
