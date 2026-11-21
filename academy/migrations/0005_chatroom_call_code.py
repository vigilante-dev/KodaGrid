import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('academy', '0004_roboticskit_skillassessment'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='call_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
