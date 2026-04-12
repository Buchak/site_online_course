from . import views
from django.urls import path, include

app_name = 'main'

urlpatterns = [
    path('courses', views.courses_list, name='courses_list'),
    path('courses/<slug:course_slug>', views.course_detail, name='course_detail')
]