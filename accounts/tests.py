from io import BytesIO, StringIO
from importlib import import_module
from types import SimpleNamespace
from unittest.mock import patch

from PIL import Image
from academy.models import TrainerProfile
from django.apps import apps
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core import mail
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connections
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .forms import StudentProfileForm
from .models import Student


class RegistrationAndAuthenticationTests(TestCase):
    password = 'A-safe-Practice-Password-482!'

    def setUp(self):
        self.settings_override = override_settings(STORAGES={
            **settings.STORAGES,
            'default': {'BACKEND': 'django.core.files.storage.InMemoryStorage'},
        })
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)

    def image_upload(self, name='student.png'):
        image = Image.new('RGB', (2, 2), color='navy')
        content = BytesIO()
        image.save(content, format='PNG')
        return SimpleUploadedFile(name, content.getvalue(), content_type='image/png')

    def registration_data(self, **overrides):
        data = {
            'username': 'amina_wanjiku',
            'name': 'Amina Wanjiku',
            'email': 'amina@example.test',
            'phone_number': '+254 700 123 456',
            'career_interest': 'Web development',
            'password1': self.password,
            'password2': self.password,
        }
        data.update(overrides)
        data['profile_picture'] = self.image_upload()
        return data

    def create_student(self, username='learner', status=Student.ApprovalStatus.PENDING, **user_options):
        User = get_user_model()
        user = User.objects.create_user(
            username=username,
            email=f'{username}@example.test',
            password=self.password,
            is_active=status == Student.ApprovalStatus.APPROVED,
            **user_options,
        )
        student = Student.objects.create(
            user=user,
            name=f'{username.title()} Learner',
            email=user.email,
            phone_number='+254700000000',
            approval_status=status,
        )
        return user, student

    def test_registration_creates_hashed_pending_inactive_user_and_complete_profile(self):
        response = self.client.post(reverse('accounts:register'), self.registration_data())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('accounts:login'))
        user = get_user_model().objects.get(username='amina_wanjiku')
        profile = Student.objects.get(user=user)
        self.assertEqual(user.email, 'amina@example.test')
        self.assertEqual(user.get_full_name(), 'Amina Wanjiku')
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(profile.approval_status, Student.ApprovalStatus.PENDING)
        self.assertEqual(profile.phone_number, '+254 700 123 456')
        self.assertTrue(profile.profile_picture.name.startswith('students/'))
        self.assertNotIn('_auth_user_id', self.client.session)

        login_page = self.client.get(reverse('accounts:login'))
        self.assertContains(login_page, 'awaiting administrator approval')

    def test_duplicate_username_is_rejected_without_creating_profile(self):
        User = get_user_model()
        User.objects.create_user(username='amina_wanjiku', password=self.password)

        response = self.client.post(reverse('accounts:register'), self.registration_data())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with that username already exists.')
        self.assertEqual(User.objects.filter(username='amina_wanjiku').count(), 1)
        self.assertFalse(Student.objects.exists())

    def test_duplicate_email_is_rejected_case_insensitively(self):
        User = get_user_model()
        User.objects.create_user(username='existing', email='AMINA@example.test', password=self.password)

        response = self.client.post(reverse('accounts:register'), self.registration_data())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An account with this email already exists.')
        self.assertEqual(User.objects.count(), 1)

    def test_invalid_registration_data_is_rejected(self):
        data = self.registration_data(email='not-an-email', username='learner_2')

        response = self.client.post(reverse('accounts:register'), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address.')
        self.assertFalse(get_user_model().objects.exists())

    def test_registration_requires_phone_and_student_photo(self):
        data = self.registration_data()
        data.pop('profile_picture')
        data.pop('phone_number')

        response = self.client.post(reverse('accounts:register'), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.', count=2)
        self.assertFalse(get_user_model().objects.exists())

    def test_password_validators_and_password_confirmation_are_enforced(self):
        common = self.client.post(
            reverse('accounts:register'),
            self.registration_data(password1='password', password2='password'),
        )
        mismatch = self.client.post(
            reverse('accounts:register'),
            self.registration_data(password2='A-different-password-789!'),
        )

        self.assertEqual(common.status_code, 200)
        self.assertContains(common, 'This password is too common.')
        self.assertEqual(mismatch.status_code, 200)
        self.assertContains(mismatch, 'The two password fields')
        self.assertFalse(get_user_model().objects.exists())

    def test_registration_form_has_one_django_form_and_no_firebase_auth(self):
        response = self.client.get(reverse('accounts:register'))
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(html.count('<form'), 1)
        self.assertIn('enctype="multipart/form-data"', html)
        self.assertIn('name="phone_number"', html)
        self.assertIn('name="profile_picture"', html)
        self.assertNotIn('firebase', html.lower())
        self.assertIn('name="career_interest"', html)

    def test_login_form_is_django_only_and_firebase_endpoint_is_removed(self):
        response = self.client.get(reverse('accounts:login'))
        html = response.content.decode().lower()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(html.count('<form'), 1)
        self.assertNotIn('firebase', html)
        self.assertEqual(self.client.get('/accounts/firebase/session/').status_code, 404)

    def test_authentication_only_firebase_dependencies_are_removed(self):
        base_dir = settings.BASE_DIR
        requirements = (base_dir / 'requirements.txt').read_text(encoding='utf-8').lower()

        self.assertNotIn('firebase', requirements)
        # The site has no npm build step; marked.js loads from a CDN in lesson.html.
        self.assertFalse((base_dir / 'package.json').exists())
        self.assertFalse((base_dir / 'package-lock.json').exists())
        self.assertFalse((base_dir / 'static/js/firebase-auth.js').exists())

    def test_pending_student_login_is_denied_with_clear_message(self):
        self.client.post(reverse('accounts:register'), self.registration_data())

        response = self.client.post(reverse('accounts:login'), {
            'username': 'amina_wanjiku',
            'password': self.password,
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'awaiting administrator approval')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_rejected_student_login_is_denied_with_clear_message(self):
        user, _student = self.create_student(status=Student.ApprovalStatus.REJECTED)

        response = self.client.post(reverse('accounts:login'), {
            'username': user.username,
            'password': self.password,
        })

        self.assertContains(response, 'Your application has not been approved.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_approved_student_can_log_in_and_log_out(self):
        user, _student = self.create_student(status=Student.ApprovalStatus.APPROVED)

        response = self.client.post(reverse('accounts:login'), {
            'username': user.username,
            'password': self.password,
        })

        self.assertRedirects(response, reverse('accounts:profile'))
        self.assertEqual(self.client.get(reverse('accounts:profile')).status_code, 200)
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('core:home'))
        self.assertRedirects(
            self.client.get(reverse('accounts:profile')),
            f'{reverse("accounts:login")}?next={reverse("accounts:profile")}',
        )

    def test_rejected_or_pending_status_blocks_a_session_even_if_user_is_active(self):
        user, _student = self.create_student(status=Student.ApprovalStatus.PENDING)
        user.is_active = True
        user.save(update_fields=('is_active',))
        self.client.force_login(user)

        response = self.client.get(reverse('accounts:profile'))

        self.assertRedirects(
            response,
            f'{reverse("accounts:login")}?next={reverse("accounts:profile")}',
        )

    def test_inactive_approved_student_cannot_log_in(self):
        user, _student = self.create_student(status=Student.ApprovalStatus.APPROVED)
        user.is_active = False
        user.save(update_fields=('is_active',))

        response = self.client.post(reverse('accounts:login'), {
            'username': user.username,
            'password': self.password,
        })

        self.assertContains(response, 'This account is inactive.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_bad_password_uses_generic_login_error(self):
        self.create_student(status=Student.ApprovalStatus.APPROVED)

        response = self.client.post(reverse('accounts:login'), {
            'username': 'learner',
            'password': 'incorrect-password',
        })

        self.assertContains(response, 'Please enter a correct username and password.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_existing_non_student_account_keeps_login_compatibility(self):
        user = get_user_model().objects.create_user(
            username='legacy', password=self.password, is_active=True,
        )
        TrainerProfile.objects.create(
            user=user,
            name='Legacy Trainer',
            email='legacy@example.test',
            headline='Programming instructor',
            bio='An existing approved trainer account.',
            skills='Python',
            is_approved=True,
        )

        response = self.client.post(reverse('accounts:login'), {
            'username': user.username,
            'password': self.password,
        })

        self.assertRedirects(response, reverse('accounts:profile'))

    def test_unlinked_non_staff_account_cannot_log_in_or_reset_its_way_past_approval(self):
        user = get_user_model().objects.create_user(
            username='legacy_orphan',
            email='orphan@example.test',
            password=self.password,
            is_active=True,
        )

        login_response = self.client.post(reverse('accounts:login'), {
            'username': user.username,
            'password': self.password,
        })
        reset_response = self.client.post(reverse('accounts:password_reset'), {
            'email': user.email,
        })

        self.assertContains(login_response, 'Please enter a correct username and password.')
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(reset_response, reverse('accounts:password_reset_done'))
        self.assertEqual(len(mail.outbox), 0)

    def test_admin_login_and_admin_access_are_preserved(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.test', password=self.password,
        )

        response = self.client.post(reverse('accounts:login'), {
            'username': admin_user.username,
            'password': self.password,
        })

        self.assertRedirects(response, reverse('accounts:profile'))
        self.assertEqual(self.client.get('/admin/').status_code, 200)

    def test_student_photo_is_only_available_to_staff(self):
        self.client.post(reverse('accounts:register'), self.registration_data())
        student = Student.objects.get(user__username='amina_wanjiku')
        photo_url = reverse('student_photo', args=(student.pk,))

        staff = get_user_model().objects.create_user(
            username='photo_reviewer', password=self.password, is_staff=True,
        )
        self.client.force_login(staff)
        response = self.client.get(photo_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        self.assertEqual(response['Cache-Control'], 'private, no-store')
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')

        learner, _profile = self.create_student(status=Student.ApprovalStatus.APPROVED)
        self.client.force_login(learner)
        response = self.client.get(photo_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'].split('?', 1)[0], reverse('admin:login'))

    def test_non_admin_cannot_access_admin(self):
        user, _student = self.create_student(status=Student.ApprovalStatus.APPROVED)
        self.client.force_login(user)

        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 302)

    def test_registration_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.get(reverse('accounts:register'))

        response = client.post(reverse('accounts:register'), self.registration_data())

        self.assertEqual(response.status_code, 403)
        self.assertFalse(get_user_model().objects.exists())

    def test_profile_form_cannot_change_approval_status(self):
        user, student = self.create_student()
        form = StudentProfileForm(data={
            'name': student.name,
            'email': student.email,
            'phone_number': student.phone_number,
            'career_interest': student.career_interest,
            'bio': 'Updated bio',
            'approval_status': Student.ApprovalStatus.APPROVED,
        }, instance=student)

        self.assertTrue(form.is_valid())
        updated = form.save()
        user.refresh_from_db()
        self.assertEqual(updated.approval_status, Student.ApprovalStatus.PENDING)
        self.assertFalse(user.is_active)

    def test_existing_administrator_can_request_a_django_password_reset(self):
        user = get_user_model().objects.create_superuser(
            username='legacy_admin', email='legacy@example.test', password=None,
        )
        user.set_unusable_password()
        user.save(update_fields=('password',))

        response = self.client.post(reverse('accounts:password_reset'), {
            'email': 'legacy@example.test',
        })

        self.assertRedirects(response, reverse('accounts:password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('legacy@example.test', mail.outbox[0].to)


class StudentApprovalAdminTests(TestCase):
    password = 'A-safe-Practice-Password-482!'

    def setUp(self):
        User = get_user_model()
        self.admin_user = User.objects.create_superuser(
            username='reviewer', email='reviewer@example.test', password=self.password,
        )
        self.client.force_login(self.admin_user)
        self.changelist_url = reverse('admin:accounts_student_changelist')

    def create_application(self, username, **user_options):
        User = get_user_model()
        user = User.objects.create_user(
            username=username,
            email=f'{username}@example.test',
            password=self.password,
            is_active=False,
            **user_options,
        )
        student = Student.objects.create(
            user=user,
            name=f'{username.title()} Student',
            email=user.email,
            phone_number='+254700000000',
        )
        return user, student

    def run_action(self, action, students):
        return self.client.post(self.changelist_url, {
            'action': action,
            '_selected_action': [str(student.pk) for student in students],
            'index': '0',
        })

    def test_admin_lists_and_filters_applications_by_status(self):
        self.create_application('pending')
        response = self.client.get(self.changelist_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pending')
        self.assertContains(response, 'Approve selected student applications')
        self.assertContains(response, 'Reject selected student applications')

    def test_admin_approves_application_and_records_reviewer_and_timestamps(self):
        user, student = self.create_application('approve_me')

        self.run_action('approve_applications', [student])

        student.refresh_from_db()
        user.refresh_from_db()
        self.assertEqual(student.approval_status, Student.ApprovalStatus.APPROVED)
        self.assertEqual(student.reviewed_by, self.admin_user)
        self.assertIsNotNone(student.reviewed_at)
        self.assertIsNotNone(student.approved_at)
        self.assertTrue(user.is_active)

    def test_admin_rejects_application_and_keeps_user_inactive(self):
        user, student = self.create_application('reject_me')

        self.run_action('reject_applications', [student])

        student.refresh_from_db()
        user.refresh_from_db()
        self.assertEqual(student.approval_status, Student.ApprovalStatus.REJECTED)
        self.assertEqual(student.reviewed_by, self.admin_user)
        self.assertIsNotNone(student.reviewed_at)
        self.assertIsNone(student.approved_at)
        self.assertFalse(user.is_active)

    def test_bulk_approval_handles_multiple_students(self):
        first_user, first = self.create_application('bulk_one')
        second_user, second = self.create_application('bulk_two')

        self.run_action('approve_applications', [first, second])

        first.refresh_from_db()
        second.refresh_from_db()
        first_user.refresh_from_db()
        second_user.refresh_from_db()
        self.assertEqual(first.approval_status, Student.ApprovalStatus.APPROVED)
        self.assertEqual(second.approval_status, Student.ApprovalStatus.APPROVED)
        self.assertTrue(first_user.is_active)
        self.assertTrue(second_user.is_active)

    def test_bulk_rejection_handles_multiple_students(self):
        first_user, first = self.create_application('reject_one')
        second_user, second = self.create_application('reject_two')

        self.run_action('reject_applications', [first, second])

        first.refresh_from_db()
        second.refresh_from_db()
        first_user.refresh_from_db()
        second_user.refresh_from_db()
        self.assertEqual(first.approval_status, Student.ApprovalStatus.REJECTED)
        self.assertEqual(second.approval_status, Student.ApprovalStatus.REJECTED)
        self.assertFalse(first_user.is_active)
        self.assertFalse(second_user.is_active)

    def test_bulk_decisions_skip_staff_and_superuser_accounts(self):
        staff, staff_student = self.create_application('staff_record', is_staff=True)
        root, root_student = self.create_application('root_record', is_superuser=True, is_staff=True)

        self.run_action('approve_applications', [staff_student, root_student])

        staff_student.refresh_from_db()
        root_student.refresh_from_db()
        staff.refresh_from_db()
        root.refresh_from_db()
        self.assertEqual(staff_student.approval_status, Student.ApprovalStatus.PENDING)
        self.assertEqual(root_student.approval_status, Student.ApprovalStatus.PENDING)
        self.assertFalse(staff.is_active)
        self.assertFalse(root.is_active)

    def test_student_cannot_run_admin_approval_action(self):
        reviewer = get_user_model().objects.create_user(
            username='student_reviewer', password=self.password, is_active=True,
        )
        target_user, target = self.create_application('target')
        self.client.force_login(reviewer)

        response = self.run_action('approve_applications', [target])

        target.refresh_from_db()
        target_user.refresh_from_db()
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(target.approval_status, Student.ApprovalStatus.PENDING)
        self.assertFalse(target_user.is_active)


class AdministratorRecoveryCommandTests(TestCase):
    def test_recover_admin_command_creates_then_restores_idempotently(self):
        output = StringIO()
        with patch('accounts.management.commands.recover_admin.getpass', side_effect=['Initial-Recovery-Password-1!', 'Initial-Recovery-Password-1!']), patch('builtins.input', return_value=''):
            call_command('recover_admin', username='codegrid', stdout=output)

        User = get_user_model()
        user = User.objects.get(username='codegrid')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password('Initial-Recovery-Password-1!'))
        self.assertEqual(
            authenticate(username='codegrid', password='Initial-Recovery-Password-1!'),
            user,
        )

        original_email = user.email
        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.save()
        with patch('accounts.management.commands.recover_admin.getpass', side_effect=['Second-Recovery-Password-2!', 'Second-Recovery-Password-2!']):
            call_command('recover_admin', username='codegrid', stdout=output)

        user.refresh_from_db()
        self.assertEqual(user.email, original_email)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password('Second-Recovery-Password-2!'))
        self.assertEqual(
            authenticate(username='codegrid', password='Second-Recovery-Password-2!'),
            user,
        )
        self.assertNotIn('Second-Recovery-Password-2!', output.getvalue())


class LegacyAccountMigrationTests(TestCase):
    def test_orphan_legacy_accounts_become_pending_and_trainers_are_preserved(self):
        User = get_user_model()
        orphan = User.objects.create_user(
            username='legacy_firebase',
            email='legacy-firebase@example.test',
            password=None,
            is_active=True,
        )
        trainer = User.objects.create_user(
            username='approved_trainer',
            email='approved-trainer@example.test',
            password='A-safe-Practice-Password-482!',
            is_active=True,
        )
        TrainerProfile.objects.create(
            user=trainer,
            name='Approved Trainer',
            email=trainer.email,
            headline='Programming instructor',
            bio='A legacy trainer profile.',
            skills='Python',
            is_approved=True,
        )

        migration = import_module('accounts.migrations.0003_pending_orphan_student_accounts')
        migration.move_orphan_accounts_to_pending(
            apps,
            SimpleNamespace(connection=connections['default']),
        )

        orphan.refresh_from_db()
        trainer.refresh_from_db()
        pending_profile = Student.objects.get(user=orphan)
        self.assertFalse(orphan.is_active)
        self.assertEqual(pending_profile.approval_status, Student.ApprovalStatus.PENDING)
        self.assertEqual(pending_profile.name, 'legacy_firebase')
        self.assertTrue(trainer.is_active)
        self.assertFalse(Student.objects.filter(user=trainer).exists())
