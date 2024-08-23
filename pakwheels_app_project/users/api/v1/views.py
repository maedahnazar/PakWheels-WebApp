from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from users.forms import UserRegisterForm 


@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            response = redirect('login')
        else:
            response = render(request, 'users/signup.html', {'form': form})
    else:
        form = UserRegisterForm()
        response = render(request, 'users/signup.html', {'form': form})

    return response

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = authenticate(
                request,
                username=username,
                password=form.cleaned_data.get('password')
            )

            if user:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                response = redirect('ad_list')
            else:
                messages.error(request, 'Invalid username or password.')
                response = render(request, 'users/login.html', {'form': form})

        else:
            for error in form.non_field_errors():
                messages.error(request, error)
                
            response = render(request, 'users/login.html', {'form': form})

    else:
        form = AuthenticationForm()
        response = render(request, 'users/login.html', {'form': form})

    return response

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")

    return redirect('ad_list')
