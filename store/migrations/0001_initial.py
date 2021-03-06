# Generated by Django 3.1 on 2021-06-16 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0003_auto_20210616_1213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200, unique=True, verbose_name='Désignation produit')),
                ('slug', models.SlugField(max_length=400, unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('price', models.IntegerField(verbose_name='prix')),
                ('images', models.ImageField(upload_to='products')),
                ('stock', models.IntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category', verbose_name='catégorie')),
            ],
        ),
    ]
