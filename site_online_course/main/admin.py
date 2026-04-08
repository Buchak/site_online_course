from django.contrib import admin

from .models import Category, Teacher, Student, Course


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_display_links = ('pk', 'name')
    ordering = ('-pk',)
    search_fields = ('pk', 'name')
    filter_horizontal = ('courses',)
    fieldsets = (
        (None, {
            'fields': ('name'),
        }),
        ('Slug', {
            'fields': ('slug',),
            'classes': ('collapse',),
        })
    )
    
    # prepopulated_fields = {'slug': ('name',)} # Slug will be auto-generated from the name field


class CourseInline(admin.StackedInline):
    model = Teacher.courses.through
    extra = 1

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [CourseInline]
    list_display = ('pk', 'name_verbose', 'email')
    list_display_links = ('pk', 'name_verbose')
    ordering = ('name_verbose',)
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
        }),   
    )
    
    def name_verbose(self, obj: Teacher):
        return f"{obj.first_name} {obj.last_name}"
    
    
class CourseInline(admin.StackedInline):
    model = Student.objects.through
    extra = 1

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [CourseInline]
    list_display = ('pk', 'name_verbose', 'email')
    list_display_links = ('pk', 'name_verbose')
    ordering = ('name_verbose',)
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
    
    def get_readonly_fields(self, request, obj=Student):
        # obj містить поточний об'єкт. 
        # Якщо obj == None, значить ми зараз на сторінці СТВОРЕННЯ нового запису
        if obj:
            # Об'єкт вже існує (це редагування) -> блокуємо поле 'customer'
            return ('age',) 
        
        # Це створення нового запису -> нічого не блокуємо
        return ()
    
    def name_verbose(self, obj: Student):
        return f"{obj.first_name} {obj.last_name}"