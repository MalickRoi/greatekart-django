# Generated by Django 3.1 on 2021-06-20 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210616_1213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Compte', 'verbose_name_plural': 'Comptes'},
        ),
    ]