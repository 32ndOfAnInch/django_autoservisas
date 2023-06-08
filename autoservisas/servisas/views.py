from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from . models import CarModel, Car, Order, Service, OrderEntry
from django.views import generic
from django.db.models.query import QuerySet
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any, Dict
from django.contrib import messages
from . forms import OrderReviewForm
from django.utils.translation import gettext_lazy as _


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

class OrderDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Order
    template_name = "core/order_detail.html"
    context_object_name = "order"
    form_class = OrderReviewForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['total_price'] = sum(entry.price for entry in self.get_object().order_entries.all())
        return context

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['reviewer'] = self.request.user
        return initial

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.car = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        messages.success(self.request, _('Review posted!'))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('order_detail', kwargs={'pk':self.get_object().pk})
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related("order_entries")
    
class UserOrderEntryListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'core/user_orderentry_list.html'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(car__owner=self.request.user)
        return qs
