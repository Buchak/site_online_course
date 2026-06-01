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


class EnrollmentForm(forms.Form):
    email = forms.EmailField(
        label='Your Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введіть ваш email',
            'class': 'form-input'
        }),
    )