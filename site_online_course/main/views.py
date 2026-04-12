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