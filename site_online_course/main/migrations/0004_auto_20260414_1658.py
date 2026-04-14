from django.db import migrations
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    Lesson = apps.get_model('main', 'Lesson')

    for lesson in Lesson.objects.all():
        if not lesson.slug:
            base_slug = slugify(lesson.title)
            lesson.slug = f"{base_slug}-{lesson.id}"

            lesson.save(update_fields=['slug'])


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0003_lesson_slug'),
    ]

    operations = [
        migrations.RunPython(generate_slugs, reverse_code=migrations.RunPython.noop),
    ]