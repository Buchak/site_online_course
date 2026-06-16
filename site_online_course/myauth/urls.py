from django.urls import path

from . import views

app_name = 'myauth'

urlpatterns = [
    path('regisetr/', views.RegisterView.as_view(), name='register'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]