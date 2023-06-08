# Generated by Django 4.2.1 on 2023-06-06 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('servisas', '0003_car_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL, verbose_name='customer'),
        ),
        migrations.AddField(
            model_name='car',
            name='note',
            field=tinymce.models.HTMLField(blank=True, max_length=50, null=True, verbose_name='Client note'),
        ),
        migrations.AddField(
            model_name='order',
            name='due_back',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='due back'),
        ),
        migrations.AddField(
            model_name='orderentry',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=18, null=True, verbose_name='total'),
        ),
    ]
