from django.conf import settings
from django.db import migrations


def move_orphan_accounts_to_pending(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Student = apps.get_model('accounts', 'Student')
    TrainerProfile = apps.get_model('academy', 'TrainerProfile')
    alias = schema_editor.connection.alias

    linked_student_ids = set(
        Student.objects.using(alias)
        .exclude(user_id=None)
        .values_list('user_id', flat=True)
    )
    trainer_user_ids = set(
        TrainerProfile.objects.using(alias)
        .exclude(user_id=None)
        .values_list('user_id', flat=True)
    )
    existing_emails = {
        email.casefold()
        for email in Student.objects.using(alias).values_list('email', flat=True)
        if email
    }

    users_by_email = {}
    for user in User.objects.using(alias).filter(is_staff=False, is_superuser=False).iterator():
        if user.pk in linked_student_ids or user.pk in trainer_user_ids:
            continue
        email = (getattr(user, 'email', '') or '').strip()
        if email:
            users_by_email.setdefault(email.casefold(), []).append((user, email))

    for normalized_email, candidates in users_by_email.items():
        if len(candidates) != 1 or normalized_email in existing_emails:
            continue
        user, email = candidates[0]
        full_name = ' '.join(part for part in (user.first_name, user.last_name) if part).strip()
        Student.objects.using(alias).create(
            user_id=user.pk,
            name=(full_name or str(getattr(user, User.USERNAME_FIELD)))[:150],
            email=email,
            approval_status='pending',
        )
        if user.is_active:
            User.objects.using(alias).filter(pk=user.pk).update(is_active=False)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_student_approval_status_student_approved_at_and_more'),
        ('academy', '0005_chatroom_call_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(move_orphan_accounts_to_pending, migrations.RunPython.noop),
    ]
