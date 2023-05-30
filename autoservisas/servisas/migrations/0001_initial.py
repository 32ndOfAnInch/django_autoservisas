# Generated by Django 4.2.1 on 2023-05-30 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutomobilioModelis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marke', models.CharField(db_index=True, max_length=50, verbose_name='marke')),
                ('modelis', models.CharField(db_index=True, max_length=50, verbose_name='modelis')),
                ('metai', models.PositiveIntegerField(db_index=True, default=2000, verbose_name='metai')),
                ('variklis', models.CharField(db_index=True, max_length=50, verbose_name='variklis')),
            ],
            options={
                'verbose_name': 'automobilio modelis',
                'verbose_name_plural': 'automobilio modeliai',
            },
        ),
        migrations.CreateModel(
            name='Automobilis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valstybinis_nr', models.CharField(db_index=True, max_length=50, verbose_name='valstybinis nr')),
                ('vin_kodas', models.CharField(db_index=True, max_length=50, verbose_name='vin kodas')),
                ('klientas', models.CharField(db_index=True, max_length=50, verbose_name='klientas')),
                ('automobilio_modelis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='automobiliai', to='servisas.automobiliomodelis', verbose_name='automobiliomodelis')),
            ],
            options={
                'verbose_name': 'automobilis',
                'verbose_name_plural': 'automobiliai',
                'ordering': ['valstybinis_nr'],
            },
        ),
        migrations.CreateModel(
            name='Paslauga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pavadinimas', models.CharField(db_index=True, max_length=50, verbose_name='pavadinimas')),
                ('kaina', models.DecimalField(db_index=True, decimal_places=2, max_digits=18, null=True, verbose_name='kaina')),
            ],
            options={
                'verbose_name': 'paslauga',
                'verbose_name_plural': 'paslaugos',
            },
        ),
        migrations.CreateModel(
            name='Uzsakymas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(auto_now_add=True, db_index=True, verbose_name='')),
                ('suma', models.DecimalField(db_index=True, decimal_places=2, max_digits=18, null=True, verbose_name='suma')),
                ('automobilis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uzsakymai', to='servisas.automobilis', verbose_name='automobilis')),
            ],
            options={
                'verbose_name': 'uzsakymas',
                'verbose_name_plural': 'uzsakymai',
            },
        ),
        migrations.CreateModel(
            name='UzsakymoEilute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kiekis', models.PositiveIntegerField(verbose_name='kiekis')),
                ('kaina', models.FloatField(verbose_name='kaina')),
                ('paslauga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uzsakymoeilutes', to='servisas.paslauga', verbose_name='uzsakymas')),
                ('uzsakymas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uzsakymoeilutes', to='servisas.uzsakymas', verbose_name='uzsakymas')),
            ],
            options={
                'verbose_name': 'uzsakymo eilute',
                'verbose_name_plural': 'uzsakymo eilutes',
            },
        ),
    ]
