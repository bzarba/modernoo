# Generated by Django 5.0.6 on 2024-06-27 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_year_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
