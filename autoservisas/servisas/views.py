from django.shortcuts import render
from django.http import HttpResponse
from . models import AutomobilioModelis, Automobilis, Uzsakymas, Paslauga, UzsakymoEilute

def index(request):
    # paslaugu kiekis
    num_paslaugos = Paslauga.objects.all().count()

    # uzsakymu kiekis
    num_uzsakymai = Uzsakymas.objects.all().count()

    # automobiliu kiekis
    num_automobiliai = Automobilis.objects.count()
    
    # perduodama i sablona zodymo pavidale

    context = {
        'num_paslaugos': num_paslaugos,
        'num_uzsakymai': num_uzsakymai,
        'num_automobiliai': num_automobiliai
    }

    return render(request, 'core/index.html', context)

def automobiliu_sarasas(request):
    return render(request, 'core/automobiliai.html', 
                  {'automobiliu_sarasas': Automobilis.objects.all()
                   })
