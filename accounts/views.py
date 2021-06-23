from django.contrib import messages, auth
from accounts.forms import RegistrationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account

# vérification de l'email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name          = form.cleaned_data['first_name']
            last_name           = form.cleaned_data['last_name']
            phone_number        = form.cleaned_data['phone_number']
            email               = form.cleaned_data['email']
            password            = form.cleaned_data['password']

            username            = email.split('@')[0]
            user                = Account.objects.create_user(
                                    first_name=first_name, last_name=last_name, 
                                    email=email, username=username, password=password)
            user.phone_number   = phone_number
            user.save()

            # activation de l'utilisateur
            current_site = get_current_site(request)
            mail_subject = 'Veuillez activer votre compte.'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Merci de vous être inscrit chez nous. Nous vous avons envoyé un e-mail de vérification à votre adresse e-mail. Veuillez le vérifier.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Vous vous êtes connecté.')
            return redirect('dashboard-page')
        else:
            messages.error(request, 'Identifiants incorrects.')
            return redirect('login-page')
    return render(request, 'accounts/login.html')


@login_required(login_url = 'login-page')
def logout_view(request):
    auth.logout(request)
    messages.success(request, 'Vous vous êtes déconnecté.')
    return redirect('login-page')


def activate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Toutes nos félicitations. Votre compte est activé.')
        return redirect('login-page')
    else:
        messages.error(request, 'Lien d\'activation invalide.')
        return redirect('register-page')


@login_required(login_url='login-page')
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')

