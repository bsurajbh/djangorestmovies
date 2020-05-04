# Generated by Django 3.0.5 on 2020-05-03 20:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1850), django.core.validators.MaxValueValidator(2020)]),
        ),
        migrations.AlterField(
            model_name='userfeedback',
            name='rating',
            field=models.FloatField(choices=[(0.0, 0.0), (0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0)]),
        ),
    ]
