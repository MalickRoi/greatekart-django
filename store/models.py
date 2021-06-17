from django.db import models
from django.urls.base import reverse
from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField('Désignation produit', max_length=200, unique=True)
    slug = models.SlugField(max_length=400, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField('prix')
    images = models.ImageField(upload_to='products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='catégorie')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product-detail-page', args=[self.category.slug, self.slug])
    
    class Meta:
        verbose_name = 'produit'
        verbose_name_plural = 'produits'
