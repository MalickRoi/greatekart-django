from django.db import models
from django.db.models.aggregates import Count
from django.urls.base import reverse
from django.db.models import Avg
from category.models import Category
from accounts.models import Account


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
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('rating'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    class Meta:
        verbose_name = 'produit'
        verbose_name_plural = 'produits'

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'Couleur'),
    ('size', 'Taille'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Désignation produit')
    user        = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Utilisateur')
    subject     = models.CharField('titre du commentaire', max_length=100, blank=True)
    review      = models.TextField('avis', max_length=500, blank=True)
    rating      = models.FloatField('évalutation')
    ip          = models.CharField(max_length=20, blank=True)
    status      = models.BooleanField('statut', default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.product.product_name} - {self.user.first_name} {self.user.last_name}' 
    
    class Meta:
        verbose_name = 'commentaire'
    


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='désignation du produit')
    image = models.ImageField(upload_to='store/products')
    
    def __str__(self):
        return f'{self.product.product_name} - {self.id}'
    
    class Meta:
        verbose_name = 'Galerie du produit'
        verbose_name_plural = 'Galeries des produits'

