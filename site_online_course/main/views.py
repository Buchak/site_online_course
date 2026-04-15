from django.shortcuts import render
from .models import Course


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
    return render(request, "main.lesson_detail.html", context=context)


def student_list(request, course_slug):
    context = {
        "students": Course.objects.get(slug=course_slug).students.all()
    }
    return render(request, "main/srudents_list.html", context=context)