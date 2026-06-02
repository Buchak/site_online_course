from . import views
from django.urls import path, include

app_name = 'main'

urlpatterns = [
    path('courses/', views.CoursesListView.as_view(), name='courses_list'),
    path('category/', views.category_list, name='category_list'),
    path('category/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('courses/<slug:course_slug>', views.CourseDetailsView.as_view(), name='course_detail'),
    path('courses/<slug:course_slug>/update-course/', views.CourseUpdateView.as_view(), name='update_course'),
    path('courses/<slug:course_slug>/delete-course/', views.CourseDeleteView.as_view(), name='delete_course'),
    path('courses/<slug:course_slug>/enrollment/', views.EnrollmentCourseView.as_view(), name='enrollment_course'),
    path('courses/<slug:course_slug>/unenrollment/', views.UnenrollmentCourseView.as_view(), name='unenrollment_course'),
    path('courses/<slug:course_slug>/students/', views.StudentsListView.as_view(), name='students_list'),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('create-course/', views.CourseCreateView.as_view(), name='create_course'),
    path('create-lesson/', views.LessonCreateView.as_view(), name='create_lesson'),
]