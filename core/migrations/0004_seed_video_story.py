from django.db import migrations


def seed_video_story(apps, schema_editor):
    VideoStory = apps.get_model('core', 'VideoStory')
    VideoStory.objects.update_or_create(
        title='See how students move from first lesson to finished project.',
        defaults={
            'kicker': 'Inside the Academy',
            'description': 'A cinematic look at coding labs, robotics builds, hackathon teamwork, portfolio reviews, and mentorship moments across the CodeSavannah learning journey.',
            'duration_label': '2 min',
            'is_featured': True,
        },
    )


def remove_video_story(apps, schema_editor):
    VideoStory = apps.get_model('core', 'VideoStory')
    VideoStory.objects.filter(title='See how students move from first lesson to finished project.').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_videostory'),
    ]

    operations = [
        migrations.RunPython(seed_video_story, remove_video_story),
    ]
