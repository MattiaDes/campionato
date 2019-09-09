from django.urls import path
from . import views

urlpatterns = [
 # ex: /squadre/ = Elenco delle squadre
 path('', views.squadre, name='squadre'),
               
 # ex: /squadre/3/ = Statistiche squadra con ID 3
 path('<int:squadra_id>/', views.statistics, name='statistics'),
               
 # ex: /squadre/calendario/ = Calendario delle partite
 path('calendario/', views.calendar, name='calendar'),
               
 # ex: /squadre/risultati/ = Elenco risultati
 path('risultati/', views.risultati, name='risultati'),
               
 # ex: /squadre/risultati/3/ = Risultati 3^ giornata di campionato
 path('risultati/<int:num_giornata>/', views.risultati_giornata, name='risultati_giornata'),
               
 # ex: /squadre/risultati/3/schedina = Schedina risultante per la 3^ giornata di campionato
 path('risultati/<int:num_giornata>/schedina/', views.schedina, name='schedina'),
               
 # ex: /squadre/classifica/ = Classifica finale
 path('classifica/', views.classifica, name='classifica'),
               
]
