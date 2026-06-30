from rest_framework.routers import DefaultRouter

from . import views
from django.urls import path, include

app_name = 'main'

routers_course = DefaultRouter()
routers_course.register('courses', views.CourseViewSet)

routers_category = DefaultRouter()
routers_category.register('categories', views.CategoryViewSet)

routers_lesson = DefaultRouter()
routers_lesson.register('lessons', views.LessonViewSet)


urlpatterns = [
    path('api/courses/', include(routers_course.urls)),
    path('api/category/', include(routers_category.urls)),
    path('api/lesson/', include(routers_lesson.urls)),
    path('api/student/', views.StudentListAPIView.as_view(), name="student_list_api"),
    path('api/teacher/', views.TeacherListAPIView.as_view(), name="teacher_list_api"),

    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/create-category', views.CategoryCreateView.as_view(), name='create_category'),
    path('category/<slug:category_slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('category/<slug:category_slug>/update-category', views.CategoryUpdateView.as_view(), name='update_category'),
    path('category/<slug:category_slug>/delete-category', views.CategoryDeleteView.as_view(), name='delete_category'),

    path('create-course/', views.CourseCreateView.as_view(), name='create_course'),
    path('courses/', views.CoursesListView.as_view(), name='courses_list'),
    path('courses/<slug:course_slug>', views.CourseDetailsView.as_view(), name='course_detail'),
    path('courses/<slug:course_slug>/students/', views.StudentsListView.as_view(), name='students_list'),
    path('courses/<slug:course_slug>/update-course/', views.CourseUpdateView.as_view(), name='update_course'),
    path('courses/<slug:course_slug>/delete-course/', views.CourseDeleteView.as_view(), name='delete_course'),

    path('courses/<slug:course_slug>/enrollment/', views.EnrollmentCourseView.as_view(), name='enrollment_course'),
    path('courses/<slug:course_slug>/unenrollment/', views.UnenrollmentCourseView.as_view(), name='unenrollment_course'),

    path('courses/<slug:course_slug>/create-lesson/', views.LessonCreateView.as_view(), name='create_lesson'),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/update-lesson/', views.LessonUpdateView.as_view(), name='update_lesson'),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/delete-lesson/', views.LessonDeleteView.as_view(), name='delete_lesson'),
    path('courses/<slug:course_slug>/<slug:lesson_slug>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]