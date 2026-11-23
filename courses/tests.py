from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from academy.models import TrainerProfile
from accounts.models import Student

from .models import Course, CourseSection, CourseTopic


class CourseSyllabusTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='Python Classroom', description='Learn Python together.', duration='8 weeks',
            category=Course.PYTHON, instructor='Trainer',
        )
        self.week1 = CourseSection.objects.create(
            course=self.course, title='Python Basics', week_label='Week 1', order=1,
            learning_objectives='Write a variable\nUse print()',
        )
        self.week2 = CourseSection.objects.create(course=self.course, title='Loops', week_label='Week 2', order=2)
        self.draft_section = CourseSection.objects.create(
            course=self.course, title='Secret Section', order=3, is_published=False,
        )
        self.intro = CourseTopic.objects.create(
            section=self.week1, title='Variables', order=1, session_format='lecture', duration_minutes=60,
            notes='Variables store values. See https://docs.python.org',
            in_class_activity='Pair up and swap two variables.',
            discussion_questions='Why name variables well?\nWhat is a type?',
            homework='Write a script that prints your name.',
            resources='Python docs | https://docs.python.org\njavascript:alert(1)',
            trainer_notes='Students often confuse = and ==.',
        )
        self.printing = CourseTopic.objects.create(section=self.week1, title='Printing', order=2, duration_minutes=30)
        self.loops = CourseTopic.objects.create(section=self.week2, title='For loops', order=1)
        self.draft_topic = CourseTopic.objects.create(
            section=self.week2, title='Hidden Draft Topic', order=2, is_published=False,
        )

    def make_user(self, username, **kwargs):
        user = User.objects.create_user(username=username, password='pass12345', **kwargs)
        Student.objects.create(
            user=user, name=username, email=f'{username}@example.test',
            approval_status=Student.ApprovalStatus.APPROVED,
        )
        return user

    def test_course_page_lists_published_syllabus_in_order(self):
        response = self.client.get(self.course.get_absolute_url())
        self.assertContains(response, 'Course Syllabus')
        self.assertContains(response, 'Write a variable')
        self.assertContains(response, 'about 2.5 hours of class time')
        content = response.content.decode()
        self.assertLess(content.index('Variables'), content.index('Printing'))
        self.assertLess(content.index('Printing'), content.index('For loops'))
        self.assertNotContains(response, 'Secret Section')
        self.assertNotContains(response, 'Hidden Draft Topic')

    def test_topic_page_shows_classroom_plan_but_hides_trainer_notes_from_students(self):
        self.client.force_login(self.make_user('learner'))
        response = self.client.get(self.intro.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        for text in ('Variables store values', 'Pair up and swap', 'Why name variables well?',
                     'prints your name', 'href="https://docs.python.org"'):
            self.assertContains(response, text)
        self.assertNotContains(response, 'confuse = and ==')
        self.assertNotContains(response, 'javascript:alert')

    def test_trainers_see_trainer_notes_and_drafts(self):
        trainer = self.make_user('coach')
        TrainerProfile.objects.create(
            user=trainer, name='Coach', email='coach@example.test', headline='h', bio='b', skills='s',
        )
        self.client.force_login(trainer)
        self.assertContains(self.client.get(self.intro.get_absolute_url()), 'confuse = and ==')
        self.assertContains(self.client.get(self.course.get_absolute_url()), 'Hidden Draft Topic')
        self.assertEqual(self.client.get(self.draft_topic.get_absolute_url()).status_code, 200)

    def test_draft_topics_are_hidden_from_public(self):
        self.assertEqual(self.client.get(self.draft_topic.get_absolute_url()).status_code, 404)
        topic_in_draft_section = CourseTopic.objects.create(section=self.draft_section, title='Inside draft')
        self.assertEqual(self.client.get(topic_in_draft_section.get_absolute_url()).status_code, 404)

    def test_topic_url_must_match_its_course(self):
        other = Course.objects.create(
            title='Other', description='d', duration='1 week', category=Course.WEB, instructor='x',
        )
        url = reverse('courses:topic', kwargs={'slug': other.slug, 'pk': self.intro.pk})
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_previous_and_next_cross_sections(self):
        response = self.client.get(self.printing.get_absolute_url())
        self.assertEqual(response.context['prev_topic'], self.intro)
        self.assertEqual(response.context['next_topic'], self.loops)
        self.assertEqual((response.context['topic_number'], response.context['topic_total']), (2, 3))

    def test_handout_needs_sign_in(self):
        self.intro.attachment.name = 'materials/course-topics/handout.pdf'
        self.intro.save()
        response = self.client.get(self.intro.get_absolute_url())
        self.assertContains(response, 'to download the handout')
        self.assertNotContains(response, 'handout.pdf')

    def test_admin_pages_for_sections_and_topics_load(self):
        admin_user = User.objects.create_superuser('boss', 'boss@example.test', 'pass12345')
        self.client.force_login(admin_user)
        urls = [
            reverse('admin:courses_course_change', args=(self.course.pk,)),
            reverse('admin:courses_coursesection_changelist'),
            reverse('admin:courses_coursesection_change', args=(self.week1.pk,)),
            reverse('admin:courses_coursesection_add'),
            reverse('admin:courses_coursetopic_changelist'),
            reverse('admin:courses_coursetopic_change', args=(self.intro.pk,)),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)
