from django.shortcuts import render,redirect
from .models import User
from .forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
# from django.conf import settings

# user = settings.AUTH_USER_MODEL



def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f' Hello {username} you registered successfully.')
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )

            login(request,new_user)
            return redirect('app:home')
    else:
        form = UserRegisterForm()

    context = {
        'form':form
    }

    return render(request,'auth/signin.html', context)


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

