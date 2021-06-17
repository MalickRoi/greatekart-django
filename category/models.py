from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField('catégorie', max_length=50, unique=True)
    # slug = models.SlugField()
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField('image', upload_to='categories', blank=True)

    class Meta:
        verbose_name = 'catégorie'
        verbose_name_plural = 'catégories'

    def __str__(self):
        return self.category_name

    def get_url(self):
            return reverse('detail-store-page', args=[self.slug])

