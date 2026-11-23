"""Regression tests for production hardening fixes."""
import shutil
import tempfile
from datetime import timedelta
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from academy.forms import TrainerApplicationForm
from academy.models import ChatMessage, ChatRoom, ClassMembership, Classroom, TrainerProfile
from accounts.forms import StudentProfileForm
from accounts.models import Student
from contact.models import ContactMessage
from events.models import Event, EventRegistration


def make_student(username, email, status=Student.ApprovalStatus.APPROVED, **user_kwargs):
    user = User.objects.create_user(username=username, password='pass12345', email=email, **user_kwargs)
    Student.objects.create(user=user, name=username.title(), email=email, approval_status=status)
    return user


class NewsletterRedirectTests(TestCase):
    def test_external_next_url_is_ignored(self):
        response = self.client.post(
            reverse('core:newsletter_signup'),
            {'email': 'reader@example.test', 'next': 'https://evil.example/phish'},
        )
        self.assertRedirects(response, reverse('core:home'), fetch_redirect_response=False)

    def test_local_next_url_is_kept(self):
        response = self.client.post(
            reverse('core:newsletter_signup'),
            {'email': 'reader@example.test', 'next': '/courses/'},
        )
        self.assertRedirects(response, '/courses/', fetch_redirect_response=False)


class ProfileForStaffAndTrainersTests(TestCase):
    def test_trainer_stays_signed_in_after_opening_portal(self):
        trainer_user = User.objects.create_user(username='coach', password='pass12345', email='coach@example.test')
        TrainerProfile.objects.create(
            user=trainer_user, name='Coach', email='coach@example.test',
            headline='Mentor', bio='Bio', skills='Python', is_approved=True,
        )
        self.client.force_login(trainer_user)
        self.assertEqual(self.client.get(reverse('accounts:profile')).status_code, 200)
        trainer_user.refresh_from_db()
        self.assertEqual(trainer_user.student_profile.approval_status, Student.ApprovalStatus.APPROVED)
        # Second request: the approval backend must still accept the session.
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

    def test_staff_profile_does_not_collide_with_existing_student_email(self):
        make_student('taken', 'shared@example.test')
        staff = User.objects.create_user(username='boss', password='pass12345', email='shared@example.test', is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get(reverse('accounts:profile')).status_code, 200)

    def test_profile_update_syncs_login_email_and_name(self):
        user = make_student('amani', 'amani@example.test')
        self.client.force_login(user)
        response = self.client.post(reverse('accounts:profile'), {
            'name': 'Amani  Njoroge', 'email': 'New@Example.test', 'phone_number': '0700000000',
            'career_interest': '', 'bio': '',
        })
        self.assertRedirects(response, reverse('accounts:profile'))
        user.refresh_from_db()
        self.assertEqual(user.email, 'new@example.test')
        self.assertEqual((user.first_name, user.last_name), ('Amani', 'Njoroge'))

    def test_profile_rejects_email_owned_by_another_login(self):
        User.objects.create_user(username='other', password='pass12345', email='other@example.test')
        user = make_student('amani', 'amani@example.test')
        form = StudentProfileForm(
            data={'name': 'Amani', 'email': 'OTHER@example.test', 'phone_number': '', 'career_interest': '', 'bio': ''},
            instance=user.student_profile,
        )
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    @override_settings(MAX_IMAGE_UPLOAD_MB=0)
    def test_oversized_profile_photo_is_rejected(self):
        user = make_student('amani', 'amani@example.test')
        gif = (b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x00\x00\x00\x00\x00'
               b',\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
        form = StudentProfileForm(
            data={'name': 'Amani', 'email': 'amani@example.test', 'phone_number': '', 'career_interest': '', 'bio': ''},
            files={'profile_picture': SimpleUploadedFile('p.gif', gif, content_type='image/gif')},
            instance=user.student_profile,
        )
        self.assertFalse(form.is_valid())
        self.assertIn('profile_picture', form.errors)

    def test_signed_in_user_is_redirected_away_from_login(self):
        self.client.force_login(make_student('amani', 'amani@example.test'))
        response = self.client.get(reverse('accounts:login'))
        self.assertRedirects(response, reverse('accounts:profile'))


class ClassroomAccessTests(TestCase):
    def setUp(self):
        self.student = make_student('denzel', 'denzel@example.test')
        self.classroom = Classroom.objects.create(name='Cohort', class_code='CALL01', description='d')
        ClassMembership.objects.create(classroom=self.classroom, student=self.student)
        self.announcements = ChatRoom.objects.create(name='Tutor Announcements', room_type='group')

    def test_classroom_video_call_loads_for_member(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('academy:video_call', kwargs={'room_code': 'CALL01'}))
        self.assertEqual(response.status_code, 200)

    def test_unknown_call_code_is_404_not_500(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('academy:video_call', kwargs={'room_code': 'NOPE99'}))
        self.assertEqual(response.status_code, 404)

    def test_external_referer_is_not_used_as_back_link(self):
        self.client.force_login(self.student)
        response = self.client.get(
            reverse('academy:video_call', kwargs={'room_code': 'CALL01'}),
            HTTP_REFERER='https://evil.example/',
        )
        self.assertEqual(response.context['back_url'], reverse('accounts:profile'))

    def test_student_cannot_post_announcement_through_classroom_form(self):
        self.client.force_login(self.student)
        self.client.post(reverse('academy:classroom'), {
            'form_action': 'send_chat_message', 'room': self.announcements.pk, 'body': 'hello all',
        })
        self.assertFalse(ChatMessage.objects.filter(room=self.announcements).exists())

    def test_unapproved_trainer_profile_cannot_create_classrooms(self):
        TrainerProfile.objects.create(
            user=self.student, name='Denzel', email='denzel@example.test',
            headline='h', bio='b', skills='s', is_approved=False,
        )
        self.client.force_login(self.student)
        self.client.post(reverse('academy:classroom'), {
            'form_action': 'create_classroom', 'name': 'Rogue Class', 'description': 'x',
            'start_date': timezone.localdate().isoformat(),
        })
        self.assertFalse(Classroom.objects.filter(name='Rogue Class').exists())


class ContactAndEventTests(TestCase):
    @override_settings(CONTACT_EMAIL='team@example.test')
    def test_contact_form_survives_mail_failure(self):
        with patch('contact.views.send_mail', side_effect=OSError('smtp down')):
            response = self.client.post(reverse('contact:contact'), {
                'name': 'Visitor', 'email': 'v@example.test', 'subject': 'Hi', 'message': 'Hello',
            })
        self.assertRedirects(response, reverse('contact:contact'))
        self.assertTrue(ContactMessage.objects.filter(email='v@example.test').exists())

    def test_past_event_rejects_registration(self):
        event = Event.objects.create(
            title='Old Hackathon', slug='old-hackathon', description='d', event_type='hackathon',
            date=timezone.now() - timedelta(days=2), location='Nairobi',
        )
        response = self.client.post(event.get_absolute_url(), {
            'name': 'Late', 'email': 'late@example.test', 'phone': '', 'message': '',
        })
        self.assertRedirects(response, event.get_absolute_url())
        self.assertFalse(EventRegistration.objects.filter(event=event).exists())


class TrainerApplicationUploadTests(TestCase):
    def test_cv_must_be_a_document(self):
        form = TrainerApplicationForm(
            data={'name': 'T', 'email': 't@example.test', 'expertise': 'Python', 'bio': 'b'},
            files={'cv': SimpleUploadedFile('cv.html', b'<script>alert(1)</script>', content_type='text/html')},
        )
        self.assertFalse(form.is_valid())
        self.assertIn('cv', form.errors)


class MediaAccessTests(TestCase):
    def setUp(self):
        self.media_root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.media_root, ignore_errors=True)
        for folder in ('gallery', 'students', 'materials'):
            (self.media_root / folder).mkdir()
            (self.media_root / folder / 'file.jpg').write_bytes(b'data')
        override = override_settings(MEDIA_ROOT=self.media_root)
        override.enable()
        self.addCleanup(override.disable)

    def test_public_media_is_served(self):
        response = self.client.get('/media/gallery/file.jpg')
        self.assertEqual(response.status_code, 200)

    def test_private_media_requires_staff(self):
        self.assertEqual(self.client.get('/media/students/file.jpg').status_code, 302)
        self.client.force_login(make_student('denzel', 'denzel@example.test'))
        self.assertEqual(self.client.get('/media/students/file.jpg').status_code, 403)
        staff = User.objects.create_user(username='boss', password='pass12345', is_staff=True)
        self.client.force_login(staff)
        response = self.client.get('/media/students/file.jpg')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment')

    def test_class_materials_require_sign_in(self):
        self.assertEqual(self.client.get('/media/materials/file.jpg').status_code, 302)
        self.client.force_login(make_student('denzel', 'denzel@example.test'))
        self.assertEqual(self.client.get('/media/materials/file.jpg').status_code, 200)

    def test_path_traversal_is_blocked(self):
        self.assertEqual(self.client.get('/media/gallery/../students/file.jpg').status_code, 404)


@override_settings(RATE_LIMIT_TRUST_FORWARDED_FOR=True)
class RateLimitTests(TestCase):
    def setUp(self):
        cache.clear()
        self.addCleanup(cache.clear)

    def test_clients_behind_proxy_get_separate_buckets(self):
        url = reverse('core:newsletter_signup')
        for _ in range(45):
            self.client.post(url, {'email': 'x'}, REMOTE_ADDR='10.0.0.1', HTTP_X_FORWARDED_FOR='1.1.1.1')
        blocked = self.client.post(url, {'email': 'x'}, REMOTE_ADDR='10.0.0.1', HTTP_X_FORWARDED_FOR='1.1.1.1')
        self.assertEqual(blocked.status_code, 429)
        other = self.client.post(url, {'email': 'x'}, REMOTE_ADDR='10.0.0.1', HTTP_X_FORWARDED_FOR='2.2.2.2')
        self.assertNotEqual(other.status_code, 429)


class ErrorPageTests(TestCase):
    def test_404_uses_branded_template(self):
        response = self.client.get('/definitely-not-a-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')


class AssessmentFlowTests(TestCase):
    def test_result_page_renders_after_submitting_assessment(self):
        answers = {f'q{i}': '1' for i in range(1, 16)}
        response = self.client.post(reverse('academy:assessment'), answers, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academy/assessment_result.html')


class TemplateSyntaxTests(TestCase):
    def test_every_template_compiles(self):
        from django.conf import settings as django_settings
        from django.template.loader import get_template

        template_dir = Path(django_settings.BASE_DIR) / 'templates'
        for template in template_dir.rglob('*.html'):
            name = template.relative_to(template_dir).as_posix()
            with self.subTest(template=name):
                get_template(name)


class ChatApiTests(TestCase):
    def setUp(self):
        self.alice = make_student('alice', 'alice@example.test')
        self.bob = make_student('bob', 'bob@example.test')
        self.eve = make_student('eve', 'eve@example.test')
        self.url = reverse('academy:chat_api')

    def post_json(self, payload):
        import json
        return self.client.post(self.url, json.dumps(payload), content_type='application/json')

    def test_directory_loads(self):
        self.client.force_login(self.alice)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        names = {entry['name'] for entry in response.json()['users']}
        self.assertIn('bob', names)

    def test_private_conversation_round_trip_and_privacy(self):
        self.client.force_login(self.alice)
        room_id = self.post_json({'action': 'start', 'user_id': self.bob.pk}).json()['id']
        self.assertEqual(self.post_json({'room': room_id, 'text': 'hi bob'}).status_code, 201)

        self.client.force_login(self.bob)
        messages_ = self.client.get(self.url, {'room': room_id}).json()['messages']
        self.assertEqual([m['text'] for m in messages_], ['hi bob'])

        self.client.force_login(self.eve)
        self.assertEqual(self.client.get(self.url, {'room': room_id}).status_code, 404)
        self.assertEqual(self.post_json({'room': room_id, 'text': 'snoop'}).status_code, 404)

    def test_students_cannot_post_announcements(self):
        self.client.force_login(self.alice)
        announcements = self.client.get(self.url).json()['announcements']
        response = self.post_json({'room': announcements, 'text': 'hello everyone'})
        self.assertEqual(response.status_code, 403)


class GameLeaderboardTests(TestCase):
    def setUp(self):
        self.url = reverse('academy:game_score')
        self.player = make_student('amara', 'amara@example.test')
        self.player.first_name, self.player.last_name = 'Amara', 'Okafor'
        self.player.save()

    def post_score(self, game, score):
        import json
        return self.client.post(self.url, json.dumps({'game': game, 'score': score}), content_type='application/json')

    def test_anonymous_scores_are_not_saved(self):
        response = self.post_score('quiz', 50)
        self.assertEqual(response.status_code, 302)

    def test_scores_are_validated(self):
        from academy.models import GameScore
        self.client.force_login(self.player)
        self.assertEqual(self.post_score('quiz', 999999).status_code, 400)
        self.assertEqual(self.post_score('chess', 10).status_code, 400)
        self.assertEqual(self.post_score('quiz', 'lots').status_code, 400)
        self.assertFalse(GameScore.objects.exists())

    def test_leaderboard_sums_best_score_per_game_this_week(self):
        from academy.models import GameScore
        self.client.force_login(self.player)
        for game, score in (('quiz', 40), ('quiz', 60), ('filler', 30)):
            self.assertEqual(self.post_score(game, score).status_code, 201)
        old = GameScore.objects.create(user=self.player, game='bugfixer', score=50)
        GameScore.objects.filter(pk=old.pk).update(created_at=timezone.now() - timedelta(days=8))

        response = self.client.get(reverse('academy:games'))
        self.assertEqual(response.context['leaderboard'], [
            {'rank': 1, 'name': 'Amara O.', 'score': 90, 'badge': '🥇'},
        ])
        self.assertNotContains(response, 'Brian M.')

    def test_empty_leaderboard_has_no_fake_players(self):
        response = self.client.get(reverse('academy:games'))
        self.assertEqual(response.context['leaderboard'], [])
        self.assertContains(response, 'No scores yet this week')


class SiteContentTests(TestCase):
    def test_about_team_comes_from_approved_trainers(self):
        TrainerProfile.objects.all().delete()
        TrainerProfile.objects.create(name='Real Trainer', email='r@example.test', headline='Lead', bio='b', skills='s')
        TrainerProfile.objects.create(name='Hidden Trainer', email='h@example.test', headline='h', bio='b', skills='s', is_approved=False)
        response = self.client.get(reverse('core:about'))
        self.assertContains(response, 'Real Trainer')
        self.assertNotContains(response, 'Hidden Trainer')
        self.assertNotContains(response, 'Brian Otieno')

    def test_footer_has_no_placeholder_social_links(self):
        response = self.client.get(reverse('core:home'))
        self.assertNotContains(response, 'href="#"')
        self.assertContains(response, 'KodaGrid')
        self.assertNotContains(response, 'CoderGrid')

    @override_settings(SOCIAL_LINKS=[('LinkedIn', 'in', 'https://www.linkedin.com/company/example')])
    def test_configured_social_links_are_rendered(self):
        response = self.client.get(reverse('core:home'))
        self.assertContains(response, 'https://www.linkedin.com/company/example')
