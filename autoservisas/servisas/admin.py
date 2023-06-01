from django.contrib import admin
from . import models

class UzsakymoEilutesInline(admin.TabularInline):
    model = models.UzsakymoEilute
    extra = 0


class UzsakymasAdmin(admin.ModelAdmin):
    list_display = ("automobilis", "data")
    inlines = [UzsakymoEilutesInline]


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ('klientas', 'automobilio_modelis', 'valstybinis_nr', 'vin_kodas')
    list_filter = ('klientas', 'automobilio_modelis')
    search_fields = ('valstybinis_nr', 'vin_kodas')


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')


class UzsakymoEiluteAdmin(admin.ModelAdmin):
    list_display = ('pavadinimas', 'kaina')


# class PaslaugosKainaAdmin(admin.ModelAdmin):
#     list_display = ('paslauga', 'automobilis', 'kaina')


# class UzsakymoKomentarasAdmin(admin.ModelAdmin):
#     list_display = ('uzsakymas', 'klientas', 'data', 'komentaras')

# admin.site.register(models.Paslaugos_kaina, PaslaugosKainaAdmin)

admin.site.register(models.AutomobilioModelis)
admin.site.register(models.Automobilis, AutomobilisAdmin)
admin.site.register(models.Uzsakymas, UzsakymasAdmin)
admin.site.register(models.Paslauga, PaslaugaAdmin)
admin.site.register(models.UzsakymoEilute)
