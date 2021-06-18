from django.db import models
from store.models import Product

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField('Id panier', max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

    class Meta:
        verbose_name = 'Panier'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Désignation produit')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='id panier')
    quantity = models.IntegerField('quantité')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product
    
    class Meta:
        verbose_name = 'courses'
        verbose_name_plural = 'courses'