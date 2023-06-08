from django.contrib.auth import get_user_model
from typing import Any, Iterable, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _   # sitas dalykas bus naudojamas vertimuose
from django.urls import reverse
from datetime import date
from tinymce.models import HTMLField

User = get_user_model()

class CarModel(models.Model):

    brand = models.CharField(_('Brand'), max_length=50, db_index=True)
    model = models.CharField(_('Model'), max_length=50, db_index=True)
    year = models.PositiveIntegerField(_("Year"), default=2000, null=True, blank=True)
    engine = models.CharField(_('Engine'), max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['brand', 'model']
        verbose_name = _("car model")
        verbose_name_plural = _("car models")

    def __str__(self):
        return f"{self.brand} {self.model} {self.year} {self.engine}"
    
    def get_absolute_url(self):
        return reverse("carmodel_detail", kwargs={"pk": self.pk})
    

class Car(models.Model):

    owner = models.CharField(_('Owner'), max_length=50, db_index=True)
    license_plate = models.CharField(_('License plate'), max_length=50, db_index=True)
    vin_code = models.CharField(_('VIN code'), max_length=50, db_index=True)
    note = HTMLField(_("Client note"), max_length=50, null=True, blank=True)
    model = models.ForeignKey(
        CarModel, 
        verbose_name=_("model"),
        related_name='cars', 
        on_delete=models.CASCADE,
        )
    
    picture = models.ImageField(
        _("picture"), 
        upload_to='core/car_pictures', 
        null=True, 
        blank=True,
    )

    customer = models.ForeignKey(
        User, 
        verbose_name=_("customer"), 
        on_delete=models.CASCADE,
        related_name="cars",
        null=True, 
        blank=True,
        )

    

    class Meta:
        ordering = ['owner']
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return f"{self.owner} {self.license_plate} {self.vin_code}"

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})
    

class Order(models.Model):

    date = models.DateField(_('Data'), auto_now_add=True, db_index=True)
    amount = models.DecimalField(_('Amount'), max_digits=18, decimal_places=2, null=True, db_index=True)
    car = models.ForeignKey(
        Car,
        verbose_name=_("car"),
        related_name="orders",
        on_delete=models.CASCADE,
    )

    due_back = models.DateField(_("due back"), null=True, blank=True, db_index=True)

    @property
    def client(self):
        return self.car.client

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"{self.date} {self.amount}"

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})
    

class Service(models.Model):

    name = models.CharField(_('Name'), max_length=50, db_index=True)
    price = models.DecimalField(_('Price'), max_digits=18, decimal_places=2, null=True, db_index=True)

    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return f"{self.name} {self.price}"

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"pk": self.pk})
    

class OrderEntry(models.Model):

    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"),
        related_name='order_entries', 
        on_delete=models.CASCADE,
        )
    service = models.ForeignKey(
        Service, 
        verbose_name=_("service"),
        related_name='order_entries', 
        on_delete=models.CASCADE,
        )
    quantity = models.PositiveIntegerField(_('quantity'))
    price = models.FloatField(_('price'))
    total = models.DecimalField(_("total"), max_digits=18, decimal_places=2, default=0, null=True, blank=True)

    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default="confirmed", db_index=True)

    class Meta:
        ordering = ['price', 'quantity']
        verbose_name = _("order entry")
        verbose_name_plural = _("order entries")

    def __str__(self):
        return f"{self.service.name} {self.quantity} {self.price}"

    def get_absolute_url(self):
        return reverse("orderentry_detail", kwargs={"pk": self.pk})
    
    def get_color(self):
        colors = {
            "confirmed": "blue",
            "in_progress": "orange",
            "completed": "green",
            "cancelled": "red",
        }
        default_color = "black"
        return colors.get(self.status, default_color)

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status)

    def save(self, *args, **kwargs):
        if self.price == 0:
            self.price = self.service.price
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)
        self.order.price = self.order.order_entries.aggregate(models.Sum("total"))["total__sum"]
        self.order.save()


class OrderReview(models.Model):
    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"), 
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    reviewer = models.ForeignKey(
        User, 
        verbose_name=_("reviewer"), 
        on_delete=models.SET_NULL,
        related_name='order_reviews',
        null=True, blank=True,
    )
    reviewed_at = models.DateTimeField(_("Reviewed"), auto_now_add=True)
    content = models.TextField(_("content"), max_length=4000)

    class Meta:
        ordering = ['-reviewed_at']
        verbose_name = _("order review")
        verbose_name_plural = _("order reviews")

    def __str__(self):
        return f"{self.reviewed_at}: {self.reviewer}"

    def get_absolute_url(self):
        return reverse("orderreview_detail", kwargs={"pk": self.pk})