from django import forms
from django.forms import fields
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Créer un mot de passe', 'class': 'form-control'}), label='Créer un mot de passe')

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe', 'class': 'form-control'}), label='Confirmer le mot de passe')
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Entrez votre prénom'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Entrez votre nom'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Entrez votre  téléphone'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Entrez votre adresse email'})
       
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas!')

