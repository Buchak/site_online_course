from django.shortcuts import render
from .models import Course, Category


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
        "categories": Category.objects.prefetch_related("courses").all()
    }
    return render(request, "main/category_list.html", context=context)

def category_detail(request, category_slug):
    context = {
        "category": Category.objects.get(slug=category_slug)
    }
    return render(request, "main/category_detail.html", context=context)