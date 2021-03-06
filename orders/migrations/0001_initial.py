# Generated by Django 3.1 on 2021-06-26 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_auto_20210620_0924'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=100, verbose_name='n°commande')),
                ('first_name', models.CharField(max_length=50, verbose_name='prénom')),
                ('last_name', models.CharField(max_length=50, verbose_name='nom')),
                ('phone', models.CharField(max_length=15, verbose_name='téléphone')),
                ('email', models.EmailField(max_length=60)),
                ('address_line_1', models.CharField(max_length=50, verbose_name='adresse de livraison 1')),
                ('address_line_2', models.CharField(blank=True, max_length=50, verbose_name='adresse de livraison 2')),
                ('country', models.CharField(max_length=50, verbose_name='Pays')),
                ('state', models.CharField(max_length=50, verbose_name='région')),
                ('city', models.CharField(max_length=50, verbose_name='ville')),
                ('order_note', models.CharField(blank=True, max_length=100, verbose_name='note de la commande')),
                ('order_total', models.FloatField(verbose_name='montant total')),
                ('tax', models.FloatField(verbose_name='tva')),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='New', max_length=100, verbose_name='état de la commande')),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('payment_method', models.CharField(max_length=100, verbose_name='Méthode de payement')),
                ('amount_paid', models.CharField(max_length=100, verbose_name='Montant payé')),
                ('status', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('product_price', models.FloatField()),
                ('ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.variation')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
