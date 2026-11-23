from django.db import migrations, models

# Admin-authored and seeded content that may mention the brand. User-generated records
# (chat messages, submissions, contact messages) are deliberately left untouched.
CONTENT_MODELS = (
    ('academy', 'Announcement'),
    ('academy', 'CommunityChallenge'),
    ('academy', 'FeePlan'),
    ('academy', 'ForumTopic'),
    ('academy', 'JobOpportunity'),
    ('academy', 'LearningMaterial'),
    ('academy', 'LearningPath'),
    ('academy', 'Lesson'),
    ('academy', 'LiveSession'),
    ('academy', 'MentorAIInteraction'),
    ('academy', 'Resource'),
    ('academy', 'RoboticsKit'),
    ('blog', 'BlogPost'),
    ('core', 'Testimonial'),
    ('core', 'VideoStory'),
    ('courses', 'Course'),
    ('events', 'Event'),
    ('gallery', 'GalleryImage'),
)


def replace_brand(apps, old, new):
    for app_label, model_name in CONTENT_MODELS:
        model = apps.get_model(app_label, model_name)
        text_fields = [
            field.name
            for field in model._meta.concrete_fields
            if isinstance(field, (models.CharField, models.TextField))
            and not isinstance(field, models.SlugField)
        ]
        for field in text_fields:
            for record in model.objects.filter(**{f'{field}__contains': old}).iterator():
                value = getattr(record, field)
                updated_value = value.replace(old, new)
                if updated_value != value:
                    setattr(record, field, updated_value)
                    record.save(update_fields=[field])


def forwards(apps, schema_editor):
    replace_brand(apps, 'CoderGrid', 'KodaGrid')


def backwards(apps, schema_editor):
    replace_brand(apps, 'KodaGrid', 'CoderGrid')


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0008_rebrand_published_content_to_codergrid'),
        ('academy', '0005_chatroom_call_code'),
        ('blog', '0001_initial'),
        ('courses', '0002_course_notes'),
        ('events', '0001_initial'),
        ('gallery', '0002_galleryimage_age_group_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
