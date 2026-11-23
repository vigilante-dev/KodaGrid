from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Student

from .models import Testimonial


class TestimonialSubmissionTests(TestCase):
    def setUp(self):
        self.url = '/testimonials/submit/'
        self.initial_testimonial_count = Testimonial.objects.count()
        self.payload = {
            'course_completed': 'Web development',
            'feedback': 'I built and published my first website.',
            'rating': '5',
        }

    def test_guest_cannot_submit_testimonial(self):
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])
        self.assertEqual(Testimonial.objects.count(), self.initial_testimonial_count)

    def test_registered_user_submission_waits_for_review(self):
        user = User.objects.create_user(
            username='learner', email='learner@example.test', password='safe-test-password',
        )
        Student.objects.create(
            user=user,
            name='Learner Student',
            email=user.email,
            approval_status=Student.ApprovalStatus.APPROVED,
        )
        self.client.force_login(user)

        response = self.client.post(self.url, self.payload)

        self.assertRedirects(response, '/')
        testimonial = Testimonial.objects.get(submitted_by=user)
        self.assertEqual(testimonial.submitted_by, user)
        self.assertEqual(testimonial.student_name, 'learner')
        self.assertFalse(testimonial.is_featured)
        self.assertEqual(Testimonial.objects.count(), self.initial_testimonial_count + 1)

    def test_invalid_submission_is_not_saved(self):
        user = User.objects.create_user(
            username='learner', email='learner@example.test', password='safe-test-password',
        )
        Student.objects.create(
            user=user,
            name='Learner Student',
            email=user.email,
            approval_status=Student.ApprovalStatus.APPROVED,
        )
        self.client.force_login(user)

        response = self.client.post(self.url, {**self.payload, 'feedback': ''})

        self.assertRedirects(response, '/')
        self.assertEqual(Testimonial.objects.count(), self.initial_testimonial_count)

# Create your tests here.
