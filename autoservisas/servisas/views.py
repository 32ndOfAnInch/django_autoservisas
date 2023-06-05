from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import CarModel, Car, Order, Service, OrderEntry
from django.views import generic
from django.db.models.query import QuerySet
from django.db.models import Q
from django.core.paginator import Paginator


def index(request):
    # paslaugu kiekis
    num_services = Service.objects.all().count()

    # uzsakymu kiekis
    num_completed_orders = OrderEntry.objects.filter(status="completed").count()

    # automobiliu kiekis
    num_cars = Car.objects.count()
    
    #apsilankymu skaitiklis
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    # perduodama i sablona zodymo pavidale

    context = {
        'num_services': num_services,
        'num_completed_orders': num_completed_orders,
        'num_cars': num_cars,
        'num_visits': num_visits,
    }

    return render(request, 'core/index.html', context)

def car_list(request):
    qs = Car.objects

    query = request.GET.get('query')
    if query:
        qs = qs.filter(Q(model__isstartwith = query))
    else:
        qs = qs.all()
    paginator = Paginator(qs, 5)
    car_list = paginator.get_page(request.GET.get('page'))
    return render(request, 'core/car_list.html', 
                  {'car_list': car_list
                   })


def car_details(request, pk: int):
    return render(request, 'core/car_details.html', {
        'car': get_object_or_404(Car, pk=pk)
    })


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 5
    context_object_name = "orders"
    template_name = "core/order_list.html"
    
    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(Q(date__icontains=query) |  #du underskorai cia yra lookup, jei per susijusius det paieska tai vietoj . imt __
                           Q(amount__icontains=query) | 
                           Q(car__owner__icontains=query))
        return qs

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "core/order_detail.html"
    context_object_name = "order"
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related("order_entries")
    

