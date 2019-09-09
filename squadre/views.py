from django.shortcuts import get_object_or_404, render

from .models import Squadra, Calendario
from django.db.models import Q, Sum
from operator import itemgetter

# Elenco delle squadre ordinate per nome
def squadre(request):
    lista_squadre = Squadra.objects.order_by('nome')
    #output = ', '.join([p.nome for p in lista_squadre])
    return render(request, 'squadre/squadre.html', {'lista_squadre': lista_squadre})

# Calendario con tutte le partite ordinate per data
def calendar(request):
    lista_partite = Calendario.objects.order_by('data')
    return render(request, 'squadre/calendario.html', {'lista_partite': lista_partite})

# Lista delle giornate di campionato
def risultati(request):
    giornate = Calendario.objects.values('giornata').distinct()
    return render(request, 'squadre/risultati.html', {'giornate': giornate})

# Risultati di una determinata giornata di campionato
def risultati_giornata(request, num_giornata):
    lista_ris_giornata = Calendario.objects.filter(giornata=num_giornata).order_by('data')
    return render(request, 'squadre/risultati_giornata.html', {'lista_ris_giornata': lista_ris_giornata, 'num_giornata': num_giornata})

# Schedina di una determinata giornata di campionato
def schedina(request, num_giornata):
    lista_ris_giornata = Calendario.objects.filter(giornata=num_giornata).order_by('data')
    return render(request, 'squadre/schedina.html', {'lista_ris_giornata': lista_ris_giornata, 'num_giornata': num_giornata})

# Statistiche di una squadra
def statistics(request, squadra_id):
    partite_squadra = Calendario.objects.filter(Q(squadraLocale=squadra_id)|Q(squadraOspite=squadra_id))
    
    def calcola_goal_punti():
        vinte=0
        pareggiate=0
        perse=0
        for conta in partite_squadra:
            if (conta.squadraLocale.id == squadra_id and conta.retiLocali > conta.retiOspiti) or (conta.squadraOspite.id == squadra_id and conta.retiOspiti > conta.retiLocali):
                vinte=vinte+1
            if (conta.squadraLocale.id == squadra_id and conta.retiLocali < conta.retiOspiti) or (conta.squadraOspite.id == squadra_id and conta.retiOspiti < conta.retiLocali):
                perse=perse+1
            if conta.retiLocali == conta.retiOspiti:
                pareggiate=pareggiate+1
        return vinte, perse, pareggiate, vinte*3+pareggiate
    
    goal_fatti_casa = Calendario.objects.filter(squadraLocale=squadra_id).aggregate(Sum('retiLocali'))
    goal_fatti_trasferta = Calendario.objects.filter(squadraOspite=squadra_id).aggregate(Sum('retiOspiti'))
    goal_subiti_casa = Calendario.objects.filter(squadraLocale=squadra_id).aggregate(Sum('retiOspiti'))
    goal_subiti_trasferta = Calendario.objects.filter(squadraOspite=squadra_id).aggregate(Sum('retiLocali'))
    
    squadra = get_object_or_404(Squadra, pk=squadra_id)
    return render(request, 'squadre/statistics.html', {'squadra': squadra, 'partite_squadra': partite_squadra, 'goal_fatti': goal_fatti_casa["retiLocali__sum"]+goal_fatti_trasferta["retiOspiti__sum"], 'goal_subiti': goal_subiti_casa["retiOspiti__sum"]+goal_subiti_trasferta["retiLocali__sum"], 'differenza_reti': (goal_fatti_casa["retiLocali__sum"]+goal_fatti_trasferta["retiOspiti__sum"])-(goal_subiti_casa["retiOspiti__sum"]+goal_subiti_trasferta["retiLocali__sum"]), 'vinte': calcola_goal_punti()[0], 'perse': calcola_goal_punti()[1], 'pareggiate': calcola_goal_punti()[2], 'punti': calcola_goal_punti()[3]})

# Classifica finale
def classifica(request):
    
    def calcola_classifica():
        lista_squadre = Squadra.objects.order_by('nome')
        classifica = {}
        for x in lista_squadre:
            partite_squadra = Calendario.objects.filter(Q(squadraLocale=x.id)|Q(squadraOspite=x.id))
            vinte=0
            pareggiate=0
            for conta in partite_squadra:
                if (conta.squadraLocale.id == x.id and conta.retiLocali > conta.retiOspiti) or (conta.squadraOspite.id == x.id and conta.retiOspiti > conta.retiLocali):
                    vinte=vinte+1
                if conta.retiLocali == conta.retiOspiti:
                    pareggiate=pareggiate+1
            classifica[x.nome] = str(vinte*3+pareggiate)
        return list(sorted(classifica.items(), key=itemgetter(1), reverse=True))

    return render(request, 'squadre/classifica.html', {'calcola_classifica': calcola_classifica()})
