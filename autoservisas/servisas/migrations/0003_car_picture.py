# Generated by Django 4.2.1 on 2023-06-02 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servisas', '0002_car_carmodel_order_orderentry_service_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='core/car_pictures', verbose_name='picture'),
        ),
    ]
