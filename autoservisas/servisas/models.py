from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class AutomobilioModelis(models.Model):

    marke = models.CharField(_('marke'), max_length=50, db_index=True)
    modelis = models.CharField(_('modelis'), max_length=50, db_index=True)
    metai = models.PositiveIntegerField(_("metai"), default=2000, null=True, blank=True)
    variklis = models.CharField(_('variklis'), max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _("automobilio modelis")
        verbose_name_plural = _("automobilio modeliai")

    def __str__(self):
        return f"Marke: {self.marke} {self.modelis} , metai: {self.metai} , variklio tipas: {self.variklis}"
    
    def get_absolute_url(self):
        return reverse("automobiliomodelis_detail", kwargs={"pk": self.pk})
    
class Automobilis(models.Model):

    valstybinis_nr = models.CharField(_('valstybinis nr'), max_length=50, db_index=True)
    vin_kodas = models.CharField(_('vin kodas'), max_length=50, db_index=True)
    klientas = models.CharField(_('klientas'), max_length=50, db_index=True)
    automobilio_modelis = models.ForeignKey(
        AutomobilioModelis, 
        verbose_name=_("automobiliomodelis"),
        related_name='automobiliai', 
        on_delete=models.CASCADE,
        )

    class Meta:
        ordering = ['valstybinis_nr']
        verbose_name = _("automobilis")
        verbose_name_plural = _("automobiliai")

    def __str__(self):
        return f"valstybinis nr: {self.valstybinis_nr} {self.automobilio_modelis} , vin kodas:  {self.vin_kodas} , klientas: {self.klientas}"

    def get_absolute_url(self):
        return reverse("automobilis_detail", kwargs={"pk": self.pk})
    

class Uzsakymas(models.Model):

    data = models.DateField(_(''), auto_now_add=True, db_index=True)
    suma = models.DecimalField(_('suma'), max_digits=18, decimal_places=2, null=True, db_index=True)
    automobilis = models.ForeignKey(
        Automobilis,
        verbose_name=_("automobilis"),
        related_name="uzsakymai",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("uzsakymas")
        verbose_name_plural = _("uzsakymai")

    def __str__(self):
        return f"uzsakymo data: {self.data} suma: {self.suma}"

    def get_absolute_url(self):
        return reverse("uzsakymas_detail", kwargs={"pk": self.pk})
    

class Paslauga(models.Model):

    pavadinimas = models.CharField(_('pavadinimas'), max_length=50, db_index=True)
    kaina = models.DecimalField(_('kaina'), max_digits=18, decimal_places=2, null=True, db_index=True)

    class Meta:
        verbose_name = _("paslauga")
        verbose_name_plural = _("paslaugos")

    def __str__(self):
        return f"paslaugos pavadinimas: {self.pavadinimas} , kaina: {self.kaina}"

    def get_absolute_url(self):
        return reverse("paslauga_detail", kwargs={"pk": self.pk})
    

class UzsakymoEilute(models.Model):

    kiekis = models.PositiveIntegerField(_('kiekis'))
    kaina = models.FloatField(_('kaina'))
    paslauga = models.ForeignKey(
        Paslauga, 
        verbose_name=_("paslauga"),
        related_name='uzsakymo_eilutes', 
        on_delete=models.CASCADE,
        )
    uzsakymas = models.ForeignKey(
        Uzsakymas, 
        verbose_name=_("uzsakymas"),
        related_name='uzsakymo_eilutes', 
        on_delete=models.CASCADE,
        )

    class Meta:
        verbose_name = _("uzsakymo eilute")
        verbose_name_plural = _("uzsakymo eilutes")

    def __str__(self):
        return f"kiekis: {self.kiekis} kaina: {self.kaina}"

    def get_absolute_url(self):
        return reverse("uzsakymoeilute_detail", kwargs={"pk": self.pk})
    
