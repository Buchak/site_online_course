from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView


# def login_view(request: HttpRequest) -> HttpResponse:
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             return redirect('main:courses_list')
#
#         return render(request, 'myauth/login.html')
#
#     username = request.POST['username']
#     password = request.POST['password']
#
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect('main:courses_list')
#
#     return render(request, 'myauth/login.html', {'error': 'Invalid username or password'})

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = ''
    success_url = reverse_lazy('')


class ProfileView(TemplateView):
    template_name = 'myauth/profile.html'


class MyLoginView(LoginView):
    template_name = 'myauth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main:courses_list')


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')