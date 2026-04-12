from django.contrib.admin import ModelAdmin
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Category, Teacher, Student, Course, Lesson


class CourseInline(admin.TabularInline):
    model = Course
    extra = 0
    fields = ('title',)
    readonly_fields = ('title',)
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CourseInline]
    list_display = ('pk', 'name', 'courses_short')
    list_display_links = ('pk', 'name')
    ordering = ('-pk',)
    search_fields = ('pk', 'name')
    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
        ('Slug', {
            'fields': ('slug',),
            'classes': ('collapse',),
        }),
    )
    
    # prepopulated_fields = {'slug': ('name',)} # Slug will be auto-generated from the name field

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('courses',)
        return ()

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('courses')

    def courses_short(self, obj: Category):
        courses = obj.courses.all()
        if len(courses) > 3:
            title = ", ".join([c.title for c in courses[:3]])
            return f"{title} ..."
        return f"{", ".join([c.title for c in courses])}"
    courses_short.short_description = 'Courses'



class CourseInline(admin.StackedInline):
    model = Teacher.courses.through
    extra = 1

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [CourseInline]
    list_display = ('pk', 'name_verbose', 'email')
    list_display_links = ('pk', 'name_verbose')
    ordering = ('first_name',)
    search_fields = ('name_verbose', 'email')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name'),
        }),
        ('Contact Info', {
            'fields': ('email',),
        }),
        ('Biography', {
            'fields': ('bio',),
            'classes': ('collapse',)
        }),   
    )
    
    def name_verbose(self, obj: Teacher):
        return f"{obj.first_name} {obj.last_name}"
    
    
class CourseInline(admin.StackedInline):
    model = Student.courses.through
    extra = 1


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [CourseInline]
    list_display = ('pk', 'name_verbose', 'email')
    list_display_links = ('pk', 'name_verbose')
    ordering = ('first_name',)
    search_fields = ('name_verbose', 'email')
    # readonly_fields = ('age',)
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name'),
        }),
        ('Contact Info', {
            'fields': ('email',),
        }),
        ('Additional Info', {
            'fields': ('age',),
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        # obj містить поточний об'єкт. 
        # Якщо obj == None, значить ми зараз на сторінці СТВОРЕННЯ нового запису
        if obj:
            # Об'єкт вже існує (це редагування) -> блокуємо поле 'customer'
            return ('age',) 
        
        # Це створення нового запису -> нічого не блокуємо
        return ()
    
    def name_verbose(self, obj: Student):
        return f"{obj.first_name} {obj.last_name}"


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ('title',)
    readonly_fields = ('title',)
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False



@admin.action(description="Publish")
def mark_published(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_published=True)

@admin.action(description="Unpublish")
def mark_unpublished(modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_published=False)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    actions = [
        mark_published,
        mark_unpublished,
    ]
    list_display = ('pk', 'title', 'category', 'price', 'created_at', 'is_published')
    list_display_links = ('pk', 'title')
    ordering = ('-pk',)
    search_fields = ('pk', 'title', 'category', 'price', 'created_at')
    readonly_fields = ('created_at',)
    filter_horizontal = ('teachers', 'students')
    fieldsets = (
        (None, {
            'fields': ('title', 'price', 'created_at'),
        }),
        ('Category', {
            'fields': ('category',),
        }),
        ('Teachers', {
            'fields': ('teachers',),
        }),
        ('Students', {
            'fields': ('students',),
            'classes': ('collapse',),
        }),
        ('Slug', {
            'fields': ('slug',),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('teachers', 'students')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'course')
    list_display_links = ('pk', 'title')
    ordering = ('-pk',)
    search_fields = ('pk', 'title', 'course')
    fieldsets = (
        (None, {
            'fields': ('title', 'course', 'order'),
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('collapse',),
        }),
        ('Video Url', {
            'fields': ('video_url',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course')
