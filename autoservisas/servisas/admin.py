from django.contrib import admin
from . import models

class OrderEntryInline(admin.TabularInline):
    model = models.OrderEntry
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ("car", "date")
    inlines = [OrderEntryInline]


class CarAdmin(admin.ModelAdmin):
    list_display = ('owner', 'model', 'license_plate', 'vin_code')
    list_filter = ('owner', 'model')
    search_fields = ('license_plate', 'vin_code')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


# class PaslaugosKainaAdmin(admin.ModelAdmin):
#     list_display = ('paslauga', 'automobilis', 'kaina')


# class UzsakymoKomentarasAdmin(admin.ModelAdmin):
#     list_display = ('uzsakymas', 'klientas', 'data', 'komentaras')

# admin.site.register(models.Paslaugos_kaina, PaslaugosKainaAdmin)

admin.site.register(models.CarModel)
admin.site.register(models.Car, CarAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.OrderEntry)
