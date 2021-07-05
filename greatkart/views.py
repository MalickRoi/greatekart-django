from django.shortcuts import render
from store.models import Product, ReviewRating

def home_view(request):
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')
    
    # obtenir les avis 
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    
    context = {
        'title': 'Accueil',
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)


