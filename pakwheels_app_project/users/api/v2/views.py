from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views import View

from users.forms import UserRegisterForm


class SignupView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/signup.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form.cleaned_data.get('username')

            return redirect('ad_list')
        
        return render(request, 'users/signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
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
                return redirect('ad_list') 
            else:
                messages.error(request, 'Invalid username or password.')

        else:
            for error in form.non_field_errors():
                messages.error(request, error)

        return render(request, 'users/login.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")

        return redirect('ad_list')
