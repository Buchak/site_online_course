from . import views
from django.urls import path, include

app_name = 'main'

urlpatterns = [
    path('courses', views.courses_list, name='courses_list'),
    path('category', views.category_list, name='category_list'),
    path('category/<slug:category_slug>', views.category_detail, name='category_detail'),
    path('courses/<slug:course_slug>', views.course_detail, name='course_detail'),
    path('courses/<slug:course_slug>/enrollment', views.enrollment_course, name='enrollment_course'),
    path('courses/<slug:course_slug>/unenrollment', views.unenrollment_course, name='unenrollment_course'),
    path('courses/<slug:course_slug>/students', views.students_list, name='students_list'),
    path('courses/<slug:course_slug>/<slug:lesson_slug>', views.lesson_detail, name='lesson_detail'),
]