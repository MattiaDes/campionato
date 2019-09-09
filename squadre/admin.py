from django.contrib import admin

# Register your models here.
from .models import Squadra, Calendario

# Filtro i contenuti per giornata e visualizzo i dati in formato tabella
class CalendarioAdmin(admin.ModelAdmin):
    list_display = ('data', 'giornata', 'squadraLocale', 'squadraOspite')
    list_filter = ['giornata']

# Possibilita' di aggiungere un calendario quando si mette una squadra
class ChoiceInline(admin.TabularInline):
    model = Calendario
    extra = 2
    fk_name = 'squadraLocale'

class SquadraAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    inlines = [ChoiceInline]

# Inserisco le tabelle Squadra e Calendario nella pagina admin
admin.site.register(Squadra,SquadraAdmin)
admin.site.register(Calendario, CalendarioAdmin)
