# Generated by Django 4.1.13 on 2024-03-17 17:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_defi_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defi',
            name='date_publication',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='defi',
            name='piece_jointe',
            field=models.FileField(blank=True, upload_to='chemin/vers/dossier'),
        ),
    ]