from django.shortcuts import render,redirect
from .models import User
from .forms import UserRegisterForm,PasswordResetForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
# from django.conf import settings

# user = settings.AUTH_USER_MODEL
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.conf import settings




def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hello {username}, you registered successfully.')
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            if new_user is not None:
                login(request, new_user)
                return redirect('app:home')
        else:
            messages.error(request, 'User already exists or there was an error with the form.')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }

    return render(request, 'auth/signin.html', context)


def login_user(request):
    if request.user.is_authenticated:
        messages.warning(request, 'yeah your already login')
        return redirect('app:home')
    
    if request.method == "POST": 
        email = request.POST.get('email')
        password = request.POST.get('psw')

        # try:
        #     user = user.objects.get(email=email)
        # except:
        #     messages.warning(request, f'user email {email} is not match')

        user = authenticate(request, email=email, password=password)
        print(user)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admindashboard:dashboard')
        
        elif user is not None:
            login(request, user)
            return redirect('/')
        
        else:
            messages.warning(request, f'user is not match please create a account ')

    
    return render(request,'auth/login.html')


def user_logout(request):
    logout(request)
    messages.warning(request, 'logout successfully')
    return redirect('auth:login')

def forget_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "auth/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                return redirect("auth:login")
            else:
                messages.error(request, 'An invalid email has been entered.')
    else:
        form = PasswordResetForm()

    context = {
        'form': form
    }

    return render(request, 'auth/forget_password.html', context)

