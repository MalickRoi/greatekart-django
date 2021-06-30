from django.db import models
from accounts.models import Account
from store.models import Product, Variation

# Create your models here.
class Payment(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id      = models.CharField(max_length=100)
    payment_method  = models.CharField('Méthode de payement', max_length=100)
    amount_paid     = models.CharField('Montant à payer', max_length=100)
    status          = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id
    
    class Meta:
        verbose_name = 'Payement'


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    user            = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number    = models.CharField('n°commande', max_length=100)
    first_name      = models.CharField('prénom', max_length=50)
    last_name       = models.CharField('nom', max_length=50)
    phone           = models.CharField('téléphone', max_length=15)
    email           = models.EmailField(max_length=60)
    address_line_1  = models.CharField('adresse de livraison 1', max_length=50)
    address_line_2  = models.CharField('adresse de livraison 2', max_length=50, blank=True)
    country         = models.CharField('Pays', max_length=50)
    state           = models.CharField('région', max_length=50)
    city            = models.CharField('ville', max_length=50)
    order_note      = models.CharField('note de la commande', max_length=100 , blank=True)
    order_total     = models.FloatField('montant total')
    tax             = models.FloatField('tva')
    status          = models.CharField('état de la commande', max_length=100, choices=STATUS, default='New')
    ip              = models.CharField(max_length=20, blank=True)
    is_ordered      = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line_1} - {self.address_line_2}'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'commande'

    
class OrderProduct(models.Model):
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    user            = models.ForeignKey(Account, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations      = models.ManyToManyField(Variation, blank=True)
    quantity        = models.IntegerField()
    product_price   = models.FloatField()
    ordered         = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'produit commandé'
        verbose_name_plural = 'produits commandés'

