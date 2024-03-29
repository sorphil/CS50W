# Generated by Django 3.1.4 on 2021-02-04 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passenger',
            name='flight',
        ),
        migrations.RemoveField(
            model_name='passenger',
            name='person',
        ),
        migrations.AddField(
            model_name='passenger',
            name='first',
            field=models.CharField(default=' ', max_length=120),
        ),
        migrations.AddField(
            model_name='passenger',
            name='flights',
            field=models.ManyToManyField(blank=True, related_name='passengers', to='flights.Flight'),
        ),
        migrations.AddField(
            model_name='passenger',
            name='last',
            field=models.CharField(default=' ', max_length=120),
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
