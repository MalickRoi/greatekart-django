from django.db.models.base import Model
from django.forms import ModelForm
from .models import ReviewRating


class ReviewForm(ModelForm):
    model = ReviewRating
    fields = ['subject', 'review', 'rating']