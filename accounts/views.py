import requests
from django.contrib import messages, auth
from django.db.models import query
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from accounts.forms import RegistrationForm, UserForm, UserProfileForm
from carts.views import _cart_id_view
from carts.models import Cart, CartItem
from orders.models import Order, OrderProduct
from .models import Account, UserProfile

# vérification de l'email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, message, send_mail

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
            
            # création du profil utilisateur
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'userprofile/default.png'
            profile.save()

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

            # messages.success(request, 'Merci de vous être inscrit chez nous. 
            # Nous vous avons envoyé un e-mail de vérification à votre adresse e-mail. Veuillez le vérifier.')
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
            try:
                cart = Cart.objects.get(cart_id=_cart_id_view(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                              
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    # Getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variatiation = item.variations.all()
                        product_variation.append(list(variatiation))
                    
                    # Getting the cart items from the user to access his product variations
                    ex_var_list = []
                    id = []
                    cart_item = CartItem.objects.filter(user=user)
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                        
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            
            auth.login(request, user)
            messages.success(request, 'Vous vous êtes connecté.')
            
            url = request.META.get('HTTP_REFERER')
            
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard-page')
        else:
            messages.error(request, 'Identifiants incorrects.')
            return redirect('login-page')
    return render(request, 'accounts/login.html')


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


@login_required(login_url = 'login-page')
def logout_view(request):
    auth.logout(request)
    messages.success(request, 'Vous vous êtes déconnecté.')
    return redirect('login-page')


@login_required(login_url = 'login-page')
def dashboard_view(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)


def forgetPassword_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # email de réinitialisation du mot de passe
            current_site = get_current_site(request)
            mail_subject = 'Réinitialisation du mot de passe'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Un e-mail de réinitialisation du mot de passe a été envoyé à votre adresse e-mail.')
            return redirect('login-page')
        else:
            messages.error(request, 'Le compte n\'existe pas.')
            return redirect('forget-pwd-page')
    return render(request, 'accounts/forget_password.html')


def reset_pwd_validate_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Veuillez réinitialiser votre mot de passe.')
        return redirect('reset-pwd-page')
    else:
        messages.error(request, 'Ce lien a expiré !')
        return redirect('login-page')


def resetPassword_view(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Votre mot de passe a été réinitialisé. Veuillez vous connecter.')
            return redirect('login-page')
        else:
            messages.error(request, 'Les mots de passe ne correspondent pas !')
            return redirect('reset-pwd-page')
    else:
        return render(request, 'accounts/reset_password.html')


@login_required(login_url='login-page')
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login-page')
def edit_profile_view(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login-page')
def change_password_view(request):
    if request.method == 'POST':
        current_password    = request.POST['current_password']
        new_password        = request.POST['new_password']
        confirm_password    = request.POST['confirm_password']
        
        user = Account.objects.get(username__exact=request.user.username)
        
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                auth.logout(request)
                messages.success(request, 'Votre mot de passe a été modifié avec succès.')
                return redirect('login-page')
            else:
                messages.error(request, 'Assurez-vous que le mot de passe actuel est correct.')
                return redirect('change-pwd-page')
        else:
            messages.error(request, 'Les deux mots de passe ne sont pas identiques.')
            return redirect('change-pwd-page')
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login-page')
def order_detail_view(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)

