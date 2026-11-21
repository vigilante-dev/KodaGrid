from django.db import migrations


CONTENT_FIELDS = {
    ('events', 'Event'): ('location',),
    ('blog', 'BlogPost'): ('title', 'excerpt', 'content'),
    ('core', 'VideoStory'): ('title', 'kicker', 'description'),
    ('core', 'Testimonial'): ('student_name', 'course_completed', 'feedback'),
}


def replace_brand(apps, schema_editor, old, new):
    for (app_label, model_name), fields in CONTENT_FIELDS.items():
        model = apps.get_model(app_label, model_name)
        for field in fields:
            queryset = model.objects.filter(**{f'{field}__icontains': old})
            for record in queryset.iterator():
                value = getattr(record, field)
                updated_value = value.replace(old, new)
                if updated_value != value:
                    setattr(record, field, updated_value)
                    record.save(update_fields=[field])


def forwards(apps, schema_editor):
    replace_brand(apps, schema_editor, 'KodaGrid', 'CoderGrid')


def backwards(apps, schema_editor):
    replace_brand(apps, schema_editor, 'CoderGrid', 'KodaGrid')


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_rebrand_published_content'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
