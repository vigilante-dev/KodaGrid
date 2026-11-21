from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import Student


class RegistrationAndAuthenticationTests(TestCase):
    password = 'A-safe-Practice-Password-482!'

    def registration_data(self, **overrides):
        data = {
            'username': 'amina_wanjiku',
            'name': 'Amina Wanjiku',
            'email': 'amina@example.test',
            'career_interest': 'Web development',
            'password1': self.password,
            'password2': self.password,
        }
        data.update(overrides)
        return data

    def test_successful_registration_creates_hashed_django_user_and_profile(self):
        response = self.client.post(reverse('accounts:register'), self.registration_data())

        self.assertRedirects(response, reverse('accounts:profile'))
        user = get_user_model().objects.get(username='amina_wanjiku')
        profile = Student.objects.get(user=user)
        self.assertEqual(user.email, 'amina@example.test')
        self.assertEqual(user.get_full_name(), 'Amina Wanjiku')
        self.assertEqual(profile.name, 'Amina Wanjiku')
        self.assertEqual(profile.career_interest, 'Web development')
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

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

    def test_invalid_email_is_rejected_and_other_values_are_kept(self):
        data = self.registration_data(email='not-an-email', username='learner_2')

        response = self.client.post(reverse('accounts:register'), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid email address.')
        self.assertContains(response, 'value="learner_2"')
        self.assertContains(response, 'value="not-an-email"')
        self.assertFalse(get_user_model().objects.exists())

    def test_password_validation_rejects_common_password(self):
        response = self.client.post(
            reverse('accounts:register'),
            self.registration_data(password1='password', password2='password'),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This password is too common.')
        self.assertFalse(get_user_model().objects.exists())

    def test_password_mismatch_is_rejected(self):
        response = self.client.post(
            reverse('accounts:register'),
            self.registration_data(password2='A-different-password-789!'),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match.")
        self.assertFalse(get_user_model().objects.exists())

    def test_register_template_has_only_the_django_form(self):
        response = self.client.get(reverse('accounts:register'))
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(html.count('<form'), 1)
        self.assertIn('action="/accounts/register/"', html)
        self.assertNotIn('firebase', html.lower())
        self.assertIn('name="career_interest"', html)
        self.assertIn('codergrid-favicon.svg', html)
        self.assertIn('CoderGrid', html)

    def test_login_session_persists_and_logout_clears_it(self):
        self.client.post(reverse('accounts:register'), self.registration_data())
        user = get_user_model().objects.get(username='amina_wanjiku')
        self.client.post(reverse('accounts:logout'))

        response = self.client.post(reverse('accounts:login'), {
            'username': user.username,
            'password': self.password,
        })

        self.assertRedirects(response, reverse('accounts:profile'))
        self.assertEqual(self.client.get(reverse('accounts:profile')).status_code, 200)
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('core:home'))
        self.assertRedirects(self.client.get(reverse('accounts:profile')), f'{reverse("accounts:login")}?next={reverse("accounts:profile")}')

    def test_incorrect_password_does_not_authenticate(self):
        get_user_model().objects.create_user(
            username='amina_wanjiku', email='amina@example.test', password=self.password,
        )

        response = self.client.post(reverse('accounts:login'), {
            'username': 'amina_wanjiku',
            'password': 'incorrect-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_page_has_one_django_auth_form(self):
        response = self.client.get(reverse('accounts:login'))
        html = response.content.decode().lower()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(html.count('<form'), 1)
        self.assertNotIn('firebase', html)

    def test_legacy_passwordless_account_can_request_a_django_password_reset(self):
        user = get_user_model().objects.create_user(
            username='legacy_learner', email='legacy@example.test', password=None,
        )
        user.set_unusable_password()
        user.save(update_fields=['password'])

        response = self.client.post(reverse('accounts:password_reset'), {
            'email': 'legacy@example.test',
        })

        self.assertRedirects(response, reverse('accounts:password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('legacy@example.test', mail.outbox[0].to)
