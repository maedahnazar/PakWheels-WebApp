from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from users.forms import UserRegisterForm 


@require_http_methods(["GET", "POST"])
def user_signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')

            return redirect('login')
        
    else:
        form = UserRegisterForm()

    return render(request, 'users/signup.html', {'form': form})

@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username=form.cleaned_data.get('username')
            user = authenticate(
                request, 
                username=username, 
                password=form.cleaned_data.get('password')
            )

            if user:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                
                return redirect('home')
            
            else:
                messages.error(request, 'Invalid username or password.')

        else:
            for error in form.non_field_errors():
                messages.error(request, error)

    else:
        form = AuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})

@require_http_methods(["POST"])
def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')
