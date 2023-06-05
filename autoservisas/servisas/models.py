from django.db import models
from django.utils.translation import gettext_lazy as _   # sitas dalykas bus naudojamas vertimuose
from django.urls import reverse


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
    
    def save(self, *args, **kwargs):
        if self.price == 0:
            self.price = self.service.price
        super().save(*args, **kwargs)
