from django import forms
from django.forms import fields
from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Créer un mot de passe', 'class': 'form-control'}), label='Créer un mot de passe')

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe', 'class': 'form-control'}), label='Confirmer le mot de passe')
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})
        
        self.fields['last_name'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                     'placeholder': 'Entrez votre nom'})
        
        self.fields['phone_number'].widget.attrs.update(
                                                        {'class': 'form-control', 
                                                         'placeholder': 'Entrez votre  téléphone'})
        
        self.fields['email'].widget.attrs.update(
                                                {'class': 'form-control', 
                                                 'placeholder': 'Entrez votre adresse email'})
       
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas!')


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})
        self.fields['last_name'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})
        self.fields['phone_number'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid': ('Chargez une image')}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture']
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['address_line_1'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})
        self.fields['address_line_2'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})
        self.fields['address_line_1'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})
        self.fields['city'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})
        self.fields['state'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})
        self.fields['country'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})
        self.fields['profile_picture'].widget.attrs.update(
                                                    {'class': 'form-control', 
                                                    'placeholder': 'Entrez votre prénom'})


