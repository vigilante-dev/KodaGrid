from datetime import timedelta

from django.db import migrations
from django.utils import timezone


def seed_content(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Event = apps.get_model('events', 'Event')
    BlogPost = apps.get_model('blog', 'BlogPost')
    GalleryImage = apps.get_model('gallery', 'GalleryImage')
    Testimonial = apps.get_model('core', 'Testimonial')

    courses = [
        {
            'title': 'Web Development',
            'slug': 'web-development',
            'category': 'web-development',
            'level': 'beginner',
            'duration': '12 weeks',
            'instructor': 'Brian Otieno',
            'is_featured': True,
            'description': 'Build responsive websites using HTML, CSS, Python, Django, deployment workflows, and portfolio-ready projects.',
            'learning_outcomes': 'Create semantic HTML pages\nStyle responsive layouts with CSS\nBuild Django views, templates, and forms\nDeploy a portfolio website',
            'requirements': 'Basic computer literacy and commitment to weekly practice.',
            'certification_details': 'Certificate awarded after completing a portfolio website and final presentation.',
        },
        {
            'title': 'Python Programming',
            'slug': 'python-programming',
            'category': 'python-programming',
            'level': 'beginner',
            'duration': '10 weeks',
            'instructor': 'Amina Wanjiku',
            'is_featured': True,
            'description': 'Learn Python fundamentals, problem solving, automation, files, APIs, and practical scripting projects.',
            'learning_outcomes': 'Write clean Python programs\nUse functions, data structures, and modules\nAutomate everyday tasks\nBuild command-line mini projects',
            'requirements': 'No programming background required.',
            'certification_details': 'Certificate awarded after completing weekly labs and a capstone script.',
        },
        {
            'title': 'Artificial Intelligence and Machine Learning',
            'slug': 'artificial-intelligence-machine-learning',
            'category': 'ai-machine-learning',
            'level': 'intermediate',
            'duration': '14 weeks',
            'instructor': 'Dr. Kevin Mwangi',
            'is_featured': True,
            'description': 'Explore AI concepts, data preparation, supervised learning, model evaluation, and responsible AI practices.',
            'learning_outcomes': 'Prepare datasets for analysis\nTrain beginner machine learning models\nEvaluate model performance\nDiscuss ethics and responsible AI',
            'requirements': 'Python basics are recommended.',
            'certification_details': 'Certificate awarded after presenting an AI project with documented findings.',
        },
        {
            'title': 'Cybersecurity Foundations',
            'slug': 'cybersecurity-foundations',
            'category': 'cybersecurity',
            'level': 'beginner',
            'duration': '8 weeks',
            'instructor': 'Grace Njeri',
            'is_featured': True,
            'description': 'Understand digital safety, networks, secure passwords, threat awareness, ethical hacking basics, and cyber career paths.',
            'learning_outcomes': 'Explain common cyber threats\nSecure accounts and devices\nUnderstand network basics\nPractice ethical security thinking',
            'requirements': 'Curiosity about how systems work.',
            'certification_details': 'Certificate awarded after completing practical security labs.',
        },
        {
            'title': 'Robotics and Physical Computing',
            'slug': 'robotics-physical-computing',
            'category': 'robotics',
            'level': 'beginner',
            'duration': '10 weeks',
            'instructor': 'Samuel Kariuki',
            'is_featured': True,
            'description': 'Design and program robots using sensors, motors, microcontrollers, teamwork, and engineering design challenges.',
            'learning_outcomes': 'Understand sensors and actuators\nProgram simple robotic behavior\nPrototype with microcontrollers\nCompete in a robotics challenge',
            'requirements': 'No electronics experience required.',
            'certification_details': 'Certificate awarded after building and demonstrating a working prototype.',
        },
        {
            'title': 'Mobile App Development',
            'slug': 'mobile-app-development',
            'category': 'mobile-app-development',
            'level': 'intermediate',
            'duration': '12 weeks',
            'instructor': 'Faith Achieng',
            'is_featured': True,
            'description': 'Plan, design, and build mobile app experiences while learning interface logic, data handling, and product thinking.',
            'learning_outcomes': 'Design mobile screens\nBuild app logic and data flows\nTest mobile experiences\nPresent a product demo',
            'requirements': 'Programming basics are helpful.',
            'certification_details': 'Certificate awarded after completing a functional app prototype.',
        },
        {
            'title': 'UI/UX Design',
            'slug': 'ui-ux-design',
            'category': 'ui-ux-design',
            'level': 'beginner',
            'duration': '8 weeks',
            'instructor': 'Naomi Chebet',
            'is_featured': False,
            'description': 'Learn research, wireframing, visual hierarchy, accessibility, prototyping, and design presentation skills.',
            'learning_outcomes': 'Conduct user research\nCreate wireframes and prototypes\nApply accessibility principles\nPresent design decisions',
            'requirements': 'No design background required.',
            'certification_details': 'Certificate awarded after completing a design case study.',
        },
        {
            'title': 'Digital Marketing',
            'slug': 'digital-marketing',
            'category': 'digital-marketing',
            'level': 'beginner',
            'duration': '6 weeks',
            'instructor': 'Moses Kiptoo',
            'is_featured': False,
            'description': 'Build practical skills in content strategy, analytics, search visibility, campaigns, and social media planning.',
            'learning_outcomes': 'Plan digital campaigns\nUnderstand SEO basics\nRead analytics reports\nCreate content calendars',
            'requirements': 'Interest in online communication and business.',
            'certification_details': 'Certificate awarded after presenting a campaign plan.',
        },
        {
            'title': 'Data Science',
            'slug': 'data-science',
            'category': 'data-science',
            'level': 'intermediate',
            'duration': '12 weeks',
            'instructor': 'Lydia Wambui',
            'is_featured': False,
            'description': 'Analyze data with Python, spreadsheets, visualization, storytelling, and beginner statistical thinking.',
            'learning_outcomes': 'Clean datasets\nCreate charts and dashboards\nTell stories with data\nBuild a data portfolio project',
            'requirements': 'Python or spreadsheet basics are recommended.',
            'certification_details': 'Certificate awarded after completing a data analysis project.',
        },
        {
            'title': 'Cloud Computing',
            'slug': 'cloud-computing',
            'category': 'cloud-computing',
            'level': 'intermediate',
            'duration': '10 weeks',
            'instructor': 'David Kimani',
            'is_featured': False,
            'description': 'Learn cloud fundamentals, deployment, storage, security basics, and modern infrastructure concepts.',
            'learning_outcomes': 'Explain cloud service models\nDeploy a simple web app\nUse storage and databases\nUnderstand cloud security basics',
            'requirements': 'Web or Python basics are recommended.',
            'certification_details': 'Certificate awarded after deploying a project to a cloud environment.',
        },
    ]

    for course in courses:
        Course.objects.update_or_create(slug=course['slug'], defaults=course)

    now = timezone.now()
    events = [
        ('AI for Beginners Workshop', 'ai-for-beginners-workshop', 'workshop', now + timedelta(days=14), 'CodeSavannah Innovation Lab', 60, 'A practical introduction to artificial intelligence, prompts, data, and responsible use.'),
        ('Youth Coding Bootcamp', 'youth-coding-bootcamp', 'bootcamp', now + timedelta(days=28), 'Nairobi Learning Hub', 45, 'A hands-on bootcamp where students build and present a responsive website.'),
        ('Cyber Safety Challenge', 'cyber-safety-challenge', 'competition', now + timedelta(days=42), 'Online', 100, 'A friendly competition focused on passwords, phishing awareness, and digital safety.'),
        ('Community Hackathon', 'community-hackathon', 'hackathon', now + timedelta(days=60), 'Partner School Auditorium', 80, 'Teams build prototypes that solve real community challenges.'),
    ]
    for title, slug, event_type, date, location, seats, description in events:
        Event.objects.update_or_create(
            slug=slug,
            defaults={
                'title': title,
                'event_type': event_type,
                'date': date,
                'location': location,
                'seats_available': seats,
                'description': description,
            },
        )

    posts = [
        ('How to Start Learning Programming as a Student', 'how-to-start-learning-programming-as-a-student', 'coding', True, 'A practical roadmap for beginners choosing their first programming path.'),
        ('Why AI Literacy Matters for Young People', 'why-ai-literacy-matters-for-young-people', 'ai', True, 'AI is becoming part of school, work, and entrepreneurship. Here is how learners can prepare.'),
        ('Building a Portfolio That Shows Real Skill', 'building-a-portfolio-that-shows-real-skill', 'career', False, 'A portfolio should show problem solving, process, and completed projects.'),
        ('Cybersecurity Habits Every Student Should Know', 'cybersecurity-habits-every-student-should-know', 'cybersecurity', False, 'Simple security habits help students protect their accounts, devices, and data.'),
    ]
    for index, (title, slug, category, featured, excerpt) in enumerate(posts):
        BlogPost.objects.update_or_create(
            slug=slug,
            defaults={
                'title': title,
                'category': category,
                'is_featured': featured,
                'excerpt': excerpt,
                'content': f'{excerpt}\n\nAt CodeSavannah Academy, we encourage students to learn by doing. Each learner builds practical projects, reflects on feedback, and develops confidence through consistent practice.',
                'date_published': now - timedelta(days=index * 7),
            },
        )

    testimonials = [
        ('Mary Achieng', 'Web Development', 'I built my first portfolio website and used it to apply for an internship. The projects made every lesson feel real.'),
        ('Kevin Mutua', 'Python Programming', 'Python finally made sense because we solved practical problems every week. I now automate tasks for my school club.'),
        ('Salma Hassan', 'Cybersecurity Foundations', 'The course helped me understand online safety and inspired me to explore cybersecurity as a career.'),
    ]
    for student_name, course_completed, feedback in testimonials:
        Testimonial.objects.update_or_create(
            student_name=student_name,
            course_completed=course_completed,
            defaults={'feedback': feedback, 'rating': 5, 'is_featured': True},
        )

    gallery_items = [
        ('Weekend Coding Lab', 'training', 'Students collaborating during a guided web development session.'),
        ('AI Workshop Demo', 'workshops', 'Learners testing AI prompts and discussing responsible use.'),
        ('Graduation Showcase', 'graduation', 'Graduates presenting portfolio projects to families and partners.'),
        ('Robotics Prototype Day', 'projects', 'Teams testing sensors, motors, and prototype ideas.'),
        ('Community Hackathon Finals', 'hackathons', 'Student teams pitching technology solutions for local challenges.'),
        ('School Outreach Visit', 'outreach', 'Mentors introducing digital skills to high school learners.'),
    ]
    for title, category, caption in gallery_items:
        GalleryImage.objects.update_or_create(
            title=title,
            defaults={'category': category, 'caption': caption, 'date_taken': now.date()},
        )


def remove_seed_content(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Event = apps.get_model('events', 'Event')
    BlogPost = apps.get_model('blog', 'BlogPost')
    GalleryImage = apps.get_model('gallery', 'GalleryImage')
    Testimonial = apps.get_model('core', 'Testimonial')

    Course.objects.filter(slug__in=[
        'web-development',
        'python-programming',
        'artificial-intelligence-machine-learning',
        'cybersecurity-foundations',
        'robotics-physical-computing',
        'mobile-app-development',
        'ui-ux-design',
        'digital-marketing',
        'data-science',
        'cloud-computing',
    ]).delete()
    Event.objects.filter(slug__in=[
        'ai-for-beginners-workshop',
        'youth-coding-bootcamp',
        'cyber-safety-challenge',
        'community-hackathon',
    ]).delete()
    BlogPost.objects.filter(slug__in=[
        'how-to-start-learning-programming-as-a-student',
        'why-ai-literacy-matters-for-young-people',
        'building-a-portfolio-that-shows-real-skill',
        'cybersecurity-habits-every-student-should-know',
    ]).delete()
    GalleryImage.objects.filter(title__in=[
        'Weekend Coding Lab',
        'AI Workshop Demo',
        'Graduation Showcase',
        'Robotics Prototype Day',
        'Community Hackathon Finals',
        'School Outreach Visit',
    ]).delete()
    Testimonial.objects.filter(student_name__in=['Mary Achieng', 'Kevin Mutua', 'Salma Hassan']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('events', '0001_initial'),
        ('blog', '0001_initial'),
        ('gallery', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_content, remove_seed_content),
    ]
