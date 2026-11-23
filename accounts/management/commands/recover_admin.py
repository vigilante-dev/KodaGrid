from getpass import getpass

from django.contrib.auth import authenticate, get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create or restore a Django administrator using an interactively entered password.'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='codegrid')

    def handle(self, *args, **options):
        UserModel = get_user_model()
        username_field = UserModel.USERNAME_FIELD
        username = options['username'].strip()
        if not username:
            raise CommandError('The administrator username cannot be empty.')

        password = getpass('New administrator password: ')
        confirmation = getpass('Confirm administrator password: ')
        if not password or password != confirmation:
            raise CommandError('The passwords were empty or did not match; no changes were made.')

        manager = UserModel._default_manager
        user = manager.filter(**{username_field: username}).first()
        created = user is None
        if created:
            required_fields = {}
            for field_name in UserModel.REQUIRED_FIELDS:
                field = UserModel._meta.get_field(field_name)
                if field.blank or field.has_default():
                    required_fields[field_name] = field.get_default()
                else:
                    required_fields[field_name] = input(f'{field_name}: ').strip()
            user = manager.create_superuser(
                **{username_field: username},
                password=password,
                **required_fields,
            )
        else:
            user.set_password(password)

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()

        authenticated_user = authenticate(
            **{username_field: username},
            password=password,
        )
        if not (
            user.check_password(password)
            and user.is_active
            and user.is_staff
            and user.is_superuser
            and authenticated_user is not None
            and authenticated_user.pk == user.pk
        ):
            raise CommandError('Administrator recovery could not be verified.')

        action = 'Created' if created else 'Restored'
        self.stdout.write(self.style.SUCCESS(f'{action} administrator {username!r}.'))
