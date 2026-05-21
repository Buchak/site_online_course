from django import forms

from . import models


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ('title', 'price', 'category', 'description')


class LessonForm(forms.ModelForm):
    class Meta:
        model = models.Lesson
        fields = ('title', 'content', 'video_url')