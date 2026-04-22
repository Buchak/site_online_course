from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

from .models import Course, Category, Student


def courses_list(request):
    context = {
        "courses": Course.objects.prefetch_related("teachers", "students").all(),
    }
    return render(request, 'main/courses_list.html', context)


def course_detail(request, course_slug):
    context = {
        "course": Course.objects.get(slug=course_slug),
    }
    return render(request, "main/course_detail.html", context=context)


def lesson_detail(request, course_slug, lesson_slug):
    course = Course.objects.get(slug=course_slug)
    context = {
        "lesson": course.lessons.get(slug=lesson_slug)
    }
    return render(request, "main/lesson_detail.html", context=context)


def students_list(request, course_slug):
    context = {
        "students": Course.objects.get(slug=course_slug).students.all()
    }
    return render(request, "main/students_list.html", context=context)


def category_list(request):
    context = {
        "categories": Category.objects.all()
    }
    return render(request, "main/category_list.html", context=context)


def category_detail(request, category_slug):
    context = {
        "category": Category.objects.prefetch_related("courses").get(slug=category_slug)
    }
    return render(request, "main/category_detail.html", context=context)


def enrollment_course(request: HttpRequest, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    if request.method == "POST" and request.POST.get("email"):
        student_email = request.POST.get("email")
        student = get_object_or_404(Student, email=student_email)

        if not course.students.filter(email=student_email).exists():
            course.students.add(student)

            return redirect('main:course_detail', course_slug=course.slug)
        else:
            return HttpResponse("Email already registered", status=400)

    context = {
        "course": course
    }

    return render(request, "main/enrollment_course.html", context=context)

def unenrollment_course(request: HttpRequest, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    if request.method == "POST" and request.POST.get("email"):
        student_email = request.POST.get("email")
        student = get_object_or_404(Student, email=student_email)

        if course.students.filter(email=student_email).exists():
            course.students.remove(student)

            return redirect('main:course_detail', course_slug=course.slug)
        else:
            return HttpResponse("Student not enrolled in course", status=400)

    context = {
        "course": course
    }

    return render(request, "main/unenrollment_course.html", context=context)