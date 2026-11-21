from django.db import migrations


def rebrand_published_content(apps, schema_editor):
    models_and_fields = {
        ('events', 'Event'): ('location',),
        ('blog', 'BlogPost'): ('title', 'excerpt', 'content'),
        ('core', 'VideoStory'): ('title', 'kicker', 'description'),
        ('core', 'Testimonial'): ('student_name', 'course_completed', 'feedback'),
    }

    for (app_label, model_name), fields in models_and_fields.items():
        model = apps.get_model(app_label, model_name)
        for field in fields:
            queryset = model.objects.filter(**{f'{field}__icontains': 'CodeSavannah'})
            for record in queryset.iterator():
                value = getattr(record, field)
                updated_value = value.replace('CodeSavannah', 'KodaGrid')
                if updated_value != value:
                    setattr(record, field, updated_value)
                    record.save(update_fields=[field])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_testimonial_submitted_by'),
    ]

    operations = [
        migrations.RunPython(rebrand_published_content, migrations.RunPython.noop),
    ]
