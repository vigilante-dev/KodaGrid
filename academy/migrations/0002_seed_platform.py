from datetime import timedelta

from django.db import migrations
from django.utils import timezone


def seed_platform(apps, schema_editor):
    LearningPath = apps.get_model('academy', 'LearningPath')
    Lesson = apps.get_model('academy', 'Lesson')
    TrainerProfile = apps.get_model('academy', 'TrainerProfile')
    Classroom = apps.get_model('academy', 'Classroom')
    Assignment = apps.get_model('academy', 'Assignment')
    LearningMaterial = apps.get_model('academy', 'LearningMaterial')
    Announcement = apps.get_model('academy', 'Announcement')
    FeePlan = apps.get_model('academy', 'FeePlan')
    ForumTopic = apps.get_model('academy', 'ForumTopic')
    ForumReply = apps.get_model('academy', 'ForumReply')
    CommunityChallenge = apps.get_model('academy', 'CommunityChallenge')
    JobOpportunity = apps.get_model('academy', 'JobOpportunity')
    Resource = apps.get_model('academy', 'Resource')
    Certificate = apps.get_model('academy', 'Certificate')

    now = timezone.now()
    path_specs = {
        'programming': ['Python', 'Java', 'JavaScript', 'TypeScript', 'C', 'C++', 'C#', 'PHP', 'Ruby', 'Kotlin', 'Dart', 'Swift', 'Rust', 'Go'],
        'web': ['HTML', 'CSS', 'JavaScript for Web', 'Bootstrap', 'TailwindCSS', 'Django', 'Flask', 'React', 'Next.js', 'Node.js'],
        'mobile': ['Flutter', 'Android Studio', 'React Native'],
        'databases': ['SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Firebase'],
        'cloud': ['AWS', 'Azure', 'Google Cloud'],
        'cybersecurity': ['Ethical Hacking', 'Networking', 'Security Fundamentals'],
        'ai': ['Machine Learning', 'Deep Learning', 'Generative AI', 'Prompt Engineering'],
    }

    featured = {'Python', 'JavaScript', 'Django', 'SQL', 'Machine Learning', 'Cybersecurity Fundamentals', 'Flutter'}
    for category, titles in path_specs.items():
        for title in titles:
            display_title = 'Cybersecurity Fundamentals' if title == 'Security Fundamentals' else title
            path, _created = LearningPath.objects.update_or_create(
                slug=display_title.lower().replace('#', 'sharp').replace('+', 'plus').replace('.', '').replace(' ', '-'),
                defaults={
                    'title': display_title,
                    'category': category,
                    'summary': f'Learn {display_title} through short lessons, guided practice, quizzes, notes, and portfolio-ready projects designed for African students and early-career builders.',
                    'level': 'beginner' if category in ['programming', 'web'] else 'intermediate',
                    'duration': '4 to 8 weeks',
                    'skill_stack': f'{display_title}, projects, debugging, documentation, teamwork',
                    'is_featured': display_title in featured,
                },
            )
            lessons = [
                ('Foundations', f'Understand the purpose, vocabulary, and core ideas behind {display_title}.', f'{display_title} starts with clear mental models. Learners study the syntax, tools, common mistakes, and how the skill is used in real technology work.', 'Write a short explanation of where this skill is used and complete the first guided practice task.'),
                ('Practice Lab', f'Apply {display_title} to a practical classroom challenge.', f'This lab turns theory into action. Students follow examples, solve small problems, compare approaches, and document what they learned.', 'Complete the practice challenge and submit notes describing your process.'),
                ('Portfolio Project', f'Build and present a small {display_title} project.', f'The project phase asks learners to design, build, test, improve, and present evidence of skill. Trainers review the work and recommend next steps.', 'Build a final mini project and prepare a five-minute demo.'),
            ]
            for order, (lesson_title, objective, content, exercise) in enumerate(lessons, start=1):
                Lesson.objects.update_or_create(
                    learning_path=path,
                    slug=lesson_title.lower().replace(' ', '-'),
                    defaults={
                        'title': lesson_title,
                        'order': order,
                        'objective': objective,
                        'content': content,
                        'exercise_prompt': exercise,
                        'quiz_question': f'What problem does {display_title} help you solve, and what is one mistake beginners should avoid?',
                        'project_prompt': f'Create a small {display_title} portfolio artifact that solves a student, school, or community problem.',
                        'notes': 'Review feedback, improve the project, and record what changed.',
                    },
                )

    trainers = [
        ('Amina Wanjiku', 'Software Engineering Lead', 'Python, Django, JavaScript, mentoring', 'Amina helps learners move from syntax to shipping complete web applications.', 'Python, Django, Web Development'),
        ('Brian Otieno', 'AI and Data Instructor', 'Machine learning, data science, prompt engineering', 'Brian teaches practical AI with responsible data habits and clear project documentation.', 'AI, Data Science, SQL'),
        ('Grace Njeri', 'Cybersecurity Mentor', 'networking, ethical hacking, digital safety', 'Grace guides students through security fundamentals, ethical thinking, and cyber career paths.', 'Cybersecurity, Networking'),
    ]
    trainer_objects = []
    for name, headline, skills, bio, courses in trainers:
        trainer, _created = TrainerProfile.objects.update_or_create(
            email=f'{name.split()[0].lower()}@codesavannah.local',
            defaults={
                'name': name,
                'headline': headline,
                'skills': skills,
                'bio': bio,
                'certifications': 'Industry mentorship, project review, learner coaching',
                'courses_taught': courses,
                'is_approved': True,
            },
        )
        trainer_objects.append(trainer)

    python_path = LearningPath.objects.filter(title='Python').first()
    ai_path = LearningPath.objects.filter(title='Machine Learning').first()
    classroom, _created = Classroom.objects.update_or_create(
        class_code='CSA101',
        defaults={
            'name': 'Python Builders Cohort',
            'trainer': trainer_objects[0],
            'learning_path': python_path,
            'description': 'A beginner-friendly classroom with weekly lessons, assignments, code reviews, and portfolio guidance.',
            'meeting_link': 'https://meet.example.com/codesavannah-python-builders',
            'start_date': now.date(),
            'is_active': True,
        },
    )
    Assignment.objects.update_or_create(
        classroom=classroom,
        title='Build a Student Study Planner',
        defaults={
            'instructions': 'Create a simple planner that stores subjects, study goals, deadlines, and completion status.',
            'due_date': now + timedelta(days=10),
            'max_score': 100,
        },
    )
    LearningMaterial.objects.update_or_create(
        classroom=classroom,
        title='Python Basics Notes',
        defaults={
            'material_type': 'notes',
            'description': 'A concise guide to variables, conditions, loops, functions, and debugging habits.',
            'learning_path': python_path,
        },
    )
    Announcement.objects.update_or_create(
        classroom=classroom,
        title='Welcome to Python Builders',
        defaults={'message': 'Prepare your laptop, install Python, and bring one problem you want to solve with code.'},
    )

    fee_plans = [
        ('Starter Code Club', 'beginner', '3500', '9500', '32000', 'Weekly guided lessons\nPractice exercises\nCommunity access\nCompletion certificate', False),
        ('Builder Bootcamp', 'intermediate', '6500', '18000', '62000', 'Project-based classes\nTrainer feedback\nPortfolio reviews\nCareer preparation', True),
        ('Advanced Engineering Track', 'advanced', '9500', '27000', '92000', 'Advanced projects\nCode reviews\nTeam collaboration\nMentor sessions', False),
        ('Professional Certification Prep', 'certification', '12000', '34000', '118000', 'Exam readiness\nMock assessments\nCertificate verification\nCareer coaching', False),
        ('Corporate Digital Skills', 'corporate', '25000', '72000', '240000', 'Custom curriculum\nTeam analytics\nLive workshops\nManagement reporting', False),
    ]
    for name, level, monthly, term, annual, features, is_featured in fee_plans:
        FeePlan.objects.update_or_create(
            name=name,
            defaults={'level': level, 'monthly_price': monthly, 'term_price': term, 'annual_price': annual, 'features': features, 'is_featured': is_featured},
        )

    topic, _created = ForumTopic.objects.update_or_create(
        title='What should I build after learning Python basics?',
        defaults={'author_name': 'Denzel', 'category': 'Projects', 'body': 'I know variables, functions, and lists. I want a project that can go into my portfolio.'},
    )
    ForumReply.objects.update_or_create(
        topic=topic,
        author_name='CodeSavannah Mentor',
        defaults={'body': 'Build a study planner, school club website backend, or expense tracker. Choose one problem and document your process.'},
    )

    challenges = [
        ('Savannah Hack Weekend', 'Hackathon', 'Build a community solution in 48 hours with a clear demo and teamwork story.', now.date() + timedelta(days=30), 'Mentorship and scholarship interviews'),
        ('Robotics Sprint', 'Competition', 'Prototype a sensor-based classroom or home automation idea.', now.date() + timedelta(days=45), 'Robotics kit grant'),
        ('AI Prompt Challenge', 'Challenge', 'Use prompt engineering to create a learning assistant for a school subject.', now.date() + timedelta(days=21), 'Featured showcase'),
    ]
    for title, challenge_type, description, deadline, prize in challenges:
        CommunityChallenge.objects.update_or_create(title=title, defaults={'challenge_type': challenge_type, 'description': description, 'deadline': deadline, 'prize': prize, 'is_active': True})

    jobs = [
        ('Junior Web Intern', 'Savannah Cloud', 'internship', 'Nairobi Hybrid', 'Support frontend and Django projects while learning professional workflows.', now.date() + timedelta(days=20)),
        ('Data Assistant Attachment', 'DataBridge Africa', 'attachment', 'Remote', 'Clean datasets, prepare dashboards, and document insights for partner teams.', now.date() + timedelta(days=25)),
        ('Freelance Landing Page Builder', 'Local Founders Network', 'freelance', 'Remote', 'Create responsive landing pages for small businesses and student founders.', None),
    ]
    for title, company, job_type, location, description, deadline in jobs:
        JobOpportunity.objects.update_or_create(title=title, company=company, defaults={'job_type': job_type, 'location': location, 'description': description, 'deadline': deadline, 'is_active': True})

    resources = [
        ('Python Beginner Cheat Sheet', 'cheatsheet', 'A quick reference for variables, conditions, loops, functions, and common errors.'),
        ('HTML Portfolio Template Checklist', 'template', 'A practical checklist for building a polished student portfolio website.'),
        ('Cyber Safety Guide for Students', 'pdf', 'A guide to passwords, phishing, device safety, and responsible online behavior.'),
        ('30-Day Coding Challenge', 'challenge', 'Daily practice prompts for learners who want steady progress and portfolio evidence.'),
    ]
    for title, resource_type, summary in resources:
        Resource.objects.update_or_create(title=title, defaults={'resource_type': resource_type, 'summary': summary, 'is_featured': True})

    Certificate.objects.update_or_create(
        student_name='Denzel Mwangi',
        course_name='Python Programming Foundations',
        defaults={'completion_date': now.date()},
    )


def remove_seed_platform(apps, schema_editor):
    LearningPath = apps.get_model('academy', 'LearningPath')
    TrainerProfile = apps.get_model('academy', 'TrainerProfile')
    FeePlan = apps.get_model('academy', 'FeePlan')
    JobOpportunity = apps.get_model('academy', 'JobOpportunity')
    Resource = apps.get_model('academy', 'Resource')
    Certificate = apps.get_model('academy', 'Certificate')
    LearningPath.objects.all().delete()
    TrainerProfile.objects.filter(email__endswith='@codesavannah.local').delete()
    FeePlan.objects.all().delete()
    JobOpportunity.objects.all().delete()
    Resource.objects.all().delete()
    Certificate.objects.filter(student_name='Denzel Mwangi').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_platform, remove_seed_platform),
    ]
