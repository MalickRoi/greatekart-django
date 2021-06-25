from django.db import models
from store.models import Product, Variation
from accounts.models import Account

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField('Id panier', max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

    class Meta:
        verbose_name = 'Panier'


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Désignation produit')
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='id panier', null=True)
    quantity = models.IntegerField('quantité')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.product_name
    
    def sub_total(self):
        return self.product.price * self.quantity    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

