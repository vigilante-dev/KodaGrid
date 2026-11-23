from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Student

from .models import Assignment, AttendanceRecord, ClassMembership, Classroom, LearningPath, Submission, TrainerProfile


class ClassroomWorkflowTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='denzel', password='pass12345')
        Student.objects.create(
            user=self.student,
            name='Denzel Student',
            email='denzel@example.test',
            approval_status=Student.ApprovalStatus.APPROVED,
        )
        self.staff = User.objects.create_user(username='admin', password='pass12345', is_staff=True)
        self.path = LearningPath.objects.create(
            title='Python Workflow Test',
            slug='python-workflow-test',
            category='programming',
            summary='Learn Python through lessons, practice, quizzes, and projects.',
            skill_stack='Python, debugging, projects',
        )
        self.trainer = TrainerProfile.objects.create(
            name='Amina Wanjiku',
            email='amina@codesavannah.local',
            headline='Software Engineering Lead',
            bio='Amina helps learners build complete applications.',
            skills='Python, Django, JavaScript',
        )
        self.classroom = Classroom.objects.create(
            name='Python Builders Cohort',
            class_code='TST101',
            trainer=self.trainer,
            learning_path=self.path,
            description='Weekly Python lessons, assignments, and portfolio feedback.',
            start_date=timezone.localdate(),
        )
        self.assignment = Assignment.objects.create(
            classroom=self.classroom,
            title='Build a Student Study Planner',
            instructions='Create a planner with subjects, goals, and deadlines.',
            due_date=timezone.now() + timedelta(days=5),
        )

    def test_student_joins_class_and_attendance_is_marked(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse('academy:classroom'),
            {'form_action': 'join_class', 'class_code': 'tst101'},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ClassMembership.objects.filter(classroom=self.classroom, student=self.student).exists())
        self.assertTrue(AttendanceRecord.objects.filter(classroom=self.classroom, student=self.student).exists())
        self.assertContains(response, 'Python Builders Cohort')
        self.assertContains(response, 'Attendance marked: 1 session')

    def test_student_submits_assignment(self):
        ClassMembership.objects.create(classroom=self.classroom, student=self.student)
        self.client.force_login(self.student)

        response = self.client.post(
            reverse('academy:classroom'),
            {
                'form_action': 'submit_assignment',
                'assignment': self.assignment.id,
                'notes': 'GitHub: https://example.com/denzel/study-planner',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        submission = Submission.objects.get(assignment=self.assignment, student=self.student)
        self.assertIn('study-planner', submission.notes)

    def test_staff_can_create_classroom(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            reverse('academy:classroom'),
            {
                'form_action': 'create_classroom',
                'name': 'AI Portfolio Lab',
                'learning_path': self.path.id,
                'description': 'A lab for building responsible AI portfolio projects.',
                'meeting_link': 'https://meet.example.com/ai-portfolio-lab',
                'start_date': timezone.localdate().isoformat(),
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Classroom.objects.filter(name='AI Portfolio Lab', is_active=True).exists())

    def test_student_cannot_create_classroom(self):
        self.client.force_login(self.student)

        response = self.client.post(
            reverse('academy:classroom'),
            {
                'form_action': 'create_classroom',
                'name': 'Unauthorized Lab',
                'learning_path': self.path.id,
                'description': 'This should not be created.',
                'start_date': timezone.localdate().isoformat(),
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Classroom.objects.filter(name='Unauthorized Lab').exists())
