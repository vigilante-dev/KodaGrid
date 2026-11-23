from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notes',
            field=models.TextField(blank=True, help_text='Course notes shown on the public course page.'),
        ),
    ]
