from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('main:courses_list')

        return render(request, 'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('main:courses_list')

    return render(request, 'myauth/login.html', {'error': 'Invalid username or password'})