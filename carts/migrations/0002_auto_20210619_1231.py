# Generated by Django 3.1 on 2021-06-19 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Panier'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'courses', 'verbose_name_plural': 'courses'},
        ),
    ]
