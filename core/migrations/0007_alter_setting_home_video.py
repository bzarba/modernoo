# Generated by Django 5.0.1 on 2024-07-09 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_setting_remove_product_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='home_video',
            field=models.ImageField(blank=True, null=True, upload_to='settings/'),
        ),
    ]
