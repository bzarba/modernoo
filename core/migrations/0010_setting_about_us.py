# Generated by Django 5.0.1 on 2024-07-11 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_brand_logo_alter_product_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='about_us',
            field=models.TextField(blank=True, null=True),
        ),
    ]
