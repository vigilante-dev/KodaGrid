from django.db import migrations


def rebrand_existing_content(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    BlogPost = apps.get_model('blog', 'BlogPost')
    VideoStory = apps.get_model('core', 'VideoStory')
    Testimonial = apps.get_model('core', 'Testimonial')

    for event in Event.objects.filter(location__icontains='TechMinds'):
        event.location = event.location.replace('TechMinds', 'CodeSavannah')
        event.save(update_fields=['location'])

    for post in BlogPost.objects.filter(content__icontains='TechMinds'):
        post.content = post.content.replace('TechMinds Academy', 'CodeSavannah Academy')
        post.save(update_fields=['content'])

    for video in VideoStory.objects.filter(description__icontains='TechMinds'):
        video.description = video.description.replace('TechMinds', 'CodeSavannah')
        video.save(update_fields=['description'])

    for testimonial in Testimonial.objects.filter(feedback__icontains='TechMinds'):
        testimonial.feedback = testimonial.feedback.replace('TechMinds', 'CodeSavannah')
        testimonial.save(update_fields=['feedback'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_seed_video_story'),
    ]

    operations = [
        migrations.RunPython(rebrand_existing_content, migrations.RunPython.noop),
    ]
