from rest_framework import serializers

from . import models


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['pk', 'title', 'price', 'created_at', 'is_published']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['pk', 'name']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['pk', 'first_name', 'last_name', 'email']


class TeacherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ['pk', 'first_name', 'last_name', 'email', 'bio']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['pk', 'first_name', 'last_name', 'email', 'age']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ['pk', 'title', 'course']


class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ['pk', 'title', 'course', 'video_url', 'content']

