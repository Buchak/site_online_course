from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


from .models import Course, Category, Student, Lesson
from . import forms, serializers


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = [
        'title',
        'price',
        'created_at',
        'is_published'
    ]
    ordering_fields = [
        'pk',
        'title',
        'price',
    ]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = ['name']
    ordering_fields = ['name']


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = ['title']
    ordering_fields = ['title']


# def courses_list(request):
#     context = {
#         "courses": Course.objects.prefetch_related("teachers", "students").all(),
#     }
#     return render(request, 'main/course_list.html', context)


class CoursesListView(ListView):
    queryset = (
        Course.objects.prefetch_related("teachers", "students")
    )
    context_object_name = "courses"


# def course_detail(request, course_slug):
#     context = {
#         "course": Course.objects.get(slug=course_slug),
#     }
#     return render(request, "main/course_detail.html", context=context)


class CourseDetailsView(DetailView):
    template_name = 'main/course_detail.html'
    model = Course
    context_object_name = 'course'
    slug_url_kwarg = 'course_slug'


# def lesson_detail(request, course_slug, lesson_slug):
#     course = Course.objects.get(slug=course_slug)
#     context = {
#         "lesson": course.lessons.get(slug=lesson_slug)
#     }
#     return render(request, "main/lesson_detail.html", context=context)


class LessonDetailView(DetailView):
    template_name = 'main/lesson_detail.html'
    model = Lesson
    context_object_name = 'lesson'
    slug_url_kwarg = 'lesson_slug'


# def students_list(request, course_slug):
#     context = {
#         "students": Course.objects.get(slug=course_slug).students.all()
#     }
#     return render(request, "main/student_list.html", context=context)


class StudentsListView(ListView):
    model = Student
    context_object_name = 'students'


# def category_list(request):
#     context = {
#         "categories": Category.objects.all()
#     }
#     return render(request, "main/category_list.html", context=context)


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'


# def category_detail(request, category_slug):
#     context = {
#         "category": Category.objects.prefetch_related("courses").get(slug=category_slug)
#     }
#     return render(request, "main/category_detail.html", context=context)


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name',]
    success_url = reverse_lazy('main:category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name',]
    slug_url_kwarg = 'category_slug'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'main:category_detail',
            kwargs={'category_slug': self.object.slug}
        )


class CategoryDeleteView(DeleteView):
    model = Category
    slug_url_kwarg = 'category_slug'
    success_url = reverse_lazy('main:category_list')


# def enrollment_course(request: HttpRequest, course_slug):
#     course = get_object_or_404(Course.objects.prefetch_related("students"), slug=course_slug)
#
#     if request.method == "POST" and request.POST.get("email"):
#         student_email = request.POST.get("email")
#         student = get_object_or_404(Student, email=student_email)
#
#         if not course.students.filter(email=student_email).exists():
#             course.students.add(student)
#
#             return redirect('main:course_detail', course_slug=course.slug)
#         else:
#             return HttpResponse("Email already registered", status=400)
#
#     context = {
#         "course": course
#     }
#
#     return render(request, "main/enrollment_course.html", context=context)


class EnrollmentCourseView(View):
    def get_course(self, course_slug):
        return get_object_or_404(Course.objects.prefetch_related("students"), slug=course_slug)

    def get(self, request: HttpRequest, course_slug):
        context = {
            'course': self.get_course(course_slug),
            'form': forms.EnrollmentForm(),
        }
        return render(request, 'main/enrollment_course.html', context=context)

    def post(self, request: HttpRequest, course_slug):
        course = self.get_course(course_slug)
        form = forms.EnrollmentForm(request.POST)

        if form.is_valid():
            student_email = form.cleaned_data['email']
            student = get_object_or_404(Student, email=student_email)

            if not course.students.filter(email=student_email).exists():
                course.students.add(student)
                return redirect('main:course_detail', course_slug=course_slug)
            else:
                return HttpResponse('Email already registered', status=400)

        context = {
            'course': course,
            'form': form,
        }
        return render(request, 'main/enrollment_course.html', context=context)


# def unenrollment_course(request: HttpRequest, course_slug):
#     course = get_object_or_404(Course.objects.prefetch_related("students"), slug=course_slug)
#
#     if request.method == "POST" and request.POST.get("email"):
#         student_email = request.POST.get("email")
#         student = get_object_or_404(Student, email=student_email)
#
#         if course.students.filter(email=student_email).exists():
#             course.students.remove(student)
#
#             return redirect('main:course_detail', course_slug=course.slug)
#         else:
#             return HttpResponse("Student not enrolled in course", status=400)
#
#     context = {
#         "course": course
#     }
#
#     return render(request, "main/unenrollment_course.html", context=context)


class UnenrollmentCourseView(View):
    def get_course(self, course_slug):
        return get_object_or_404(Course.objects.prefetch_related('students'), slug=course_slug)

    def get(self, request: HttpRequest, course_slug):
        context = {
            'course': self.get_course(course_slug),
            'form': forms.EnrollmentForm(),
        }
        return render(request, "main/unenrollment_course.html", context=context)

    def post(self, request: HttpRequest, course_slug):
        course = self.get_course(course_slug)
        form = forms.EnrollmentForm(request.POST)

        if form.is_valid():
            student_email = form.cleaned_data['email']
            student = get_object_or_404(Student, email=student_email)

            if course.students.filter(email=student_email).exists():
                course.students.remove(student)
                return redirect('main:course_detail', course_slug=course_slug)
            else:
                return HttpResponse("Student not enrolled in course", status=400)

        context = {
            'course': course,
            'form': form,
        }
        return render(request, 'main/unenrollment_course.html', context=context)


# def create_course(request: HttpRequest):
#     if request.method == 'POST':
#         form = forms.CourseForm(request.POST)
#         if form.is_valid():
#             Course.objects.create(**form.cleaned_data)
#             return redirect('main:courses_list')
#     else:
#         form = forms.CourseForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, "main/course_form.html", context=context)


class CourseCreateView(CreateView):
    model = Course
    form_class = forms.CourseForm

    def get_success_url(self):
        return reverse(
            'main:course_detail',
            kwargs={'course_slug': self.object.slug}
        )


class CourseUpdateView(UpdateView):
    model = Course
    form_class = forms.CourseForm
    template_name_suffix = '_update_form'
    slug_url_kwarg = 'course_slug'

    def get_success_url(self):
        return reverse(
            'main:course_detail',
            kwargs={'course_slug': self.object.slug}
        )


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('main:courses_list')
    template_name_suffix = '_delete'
    slug_url_kwarg = 'course_slug'


# def create_lesson(request: HttpRequest):
#     if request.method == 'POST':
#         form = forms.LessonForm(request.POST)
#         if form.is_valid():
#             Lesson.objects.create(**form.cleaned_data)
#             return redirect('main:courses_list')
#     else:
#         form = forms.LessonForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, "main/lesson_form.html", context=context)


class LessonCreateView(CreateView):
    model = Lesson
    fields = ['title', 'content', 'video_url']
    slug_url_kwarg = 'course_slug'

    def form_valid(self, form):
        course_slug = self.kwargs.get('course_slug')
        course = get_object_or_404(Course, slug=course_slug)
        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'main:course_detail',
            kwargs={'course_slug': self.object.course.slug}
        )


class LessonUpdateView(UpdateView):
    model = Lesson
    fields = ['title', 'content', 'video_url']
    slug_url_kwarg = 'lesson_slug'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'main:lesson_detail',
            kwargs={'course_slug': self.kwargs.get('course_slug'),
                    'lesson_slug': self.object.slug}
        )


class LessonDeleteView(DeleteView):
    model = Lesson
    slug_url_kwarg = 'lesson_slug'
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse(
            'main:course_detail',
            kwargs={'course_slug': self.kwargs.get('course_slug')}
        )


