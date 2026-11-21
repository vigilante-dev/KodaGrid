from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, FormView, ListView, TemplateView

from .forms import AssignmentSubmissionForm, ChatMessageForm, CreateClassroomForm, JoinClassForm, MentorAIForm, MentorshipBookingForm, TrainerApplicationForm
from .models import (
    Announcement,
    Assignment,
    RoboticsKit,
    SkillAssessment,
    AttendanceRecord,
    Certificate,
    ChatMessage,
    ChatRoom,
    ClassMembership,
    Classroom,
    CommunityChallenge,
    FeePlan,
    ForumTopic,
    JobOpportunity,
    LearningMaterial,
    LearningPath,
    LiveSession,
    MentorAIInteraction,
    Resource,
    Submission,
    TrainerProfile,
)


class LearningPathListView(ListView):
    model = LearningPath
    template_name = 'academy/learning_path_list.html'
    context_object_name = 'paths'
    paginate_by = 12

    def get_queryset(self):
        queryset = LearningPath.objects.annotate(lesson_count=Count('lessons')).order_by('category', 'title')
        query = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '').strip()
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(skill_stack__icontains=query))
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = LearningPath.CATEGORIES
        context['active_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class LearningPathDetailView(DetailView):
    model = LearningPath
    template_name = 'academy/learning_path_detail.html'
    context_object_name = 'path'


class HighSchoolDivisionView(TemplateView):
    template_name = 'academy/high_school.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['boys_focus'] = ['Coding skills', 'Leadership', 'Entrepreneurship', 'Robotics', 'STEM competitions']
        context['girls_focus'] = ['Women in Tech mentorship', 'Programming foundations', 'Scholarship readiness', 'Leadership labs', 'Confidence through building']
        return context


class CollegeDivisionView(TemplateView):
    template_name = 'academy/college.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracks'] = [
            'Career preparation and interview practice',
            'Internship and attachment matching',
            'Portfolio and GitHub project reviews',
            'Freelancing readiness and client communication',
            'Startup incubation and product validation',
            'Industry mentorship with practicing technologists',
        ]
        return context


class TrainerDirectoryView(FormView):
    template_name = 'academy/trainers.html'
    form_class = TrainerApplicationForm
    success_url = reverse_lazy('academy:trainers')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainers'] = TrainerProfile.objects.filter(is_approved=True)
        context['booking_form'] = kwargs.get('booking_form') or MentorshipBookingForm()
        return context

    def post(self, request, *args, **kwargs):
        form_type = request.POST.get('form_type')
        if form_type == 'booking':
            booking_form = MentorshipBookingForm(request.POST)
            if booking_form.is_valid():
                booking_form.save()
                messages.success(request, 'Mentorship request submitted. Our team will confirm your session.')
                return redirect(self.success_url)
            return self.render_to_response(self.get_context_data(form=self.get_form(), booking_form=booking_form))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Trainer application received. Our academic team will review it.')
        return super().form_valid(form)


class FeePlanListView(ListView):
    model = FeePlan
    template_name = 'academy/fees.html'
    context_object_name = 'plans'


class CommunityHubView(TemplateView):
    template_name = 'academy/community.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = ForumTopic.objects.prefetch_related('replies')[:6]
        context['challenges'] = CommunityChallenge.objects.filter(is_active=True)[:6]
        return context


class JobBoardView(ListView):
    model = JobOpportunity
    template_name = 'academy/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 9

    def get_queryset(self):
        queryset = JobOpportunity.objects.filter(is_active=True)
        job_type = self.request.GET.get('type', '').strip()
        query = self.request.GET.get('q', '').strip()
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(company__icontains=query) | Q(description__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_types'] = JobOpportunity.JOB_TYPES
        context['active_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ResourceCenterView(ListView):
    model = Resource
    template_name = 'academy/resources.html'
    context_object_name = 'resources'
    paginate_by = 12

    def get_queryset(self):
        queryset = Resource.objects.all()
        resource_type = self.request.GET.get('type', '').strip()
        query = self.request.GET.get('q', '').strip()
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(summary__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_types'] = Resource.RESOURCE_TYPES
        context['active_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ClassroomHubView(LoginRequiredMixin, TemplateView):
    template_name = 'academy/classroom.html'

    def user_can_manage(self):
        user = self.request.user
        return user.is_staff or user.is_superuser or hasattr(user, 'trainer_profile')

    def get_user_classrooms(self):
        queryset = Classroom.objects.filter(is_active=True).select_related('trainer', 'learning_path')
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        return queryset.filter(memberships__student=self.request.user).distinct()

    def get_user_assignments(self):
        classroom_ids = self.get_user_classrooms().values_list('id', flat=True)
        return Assignment.objects.filter(classroom_id__in=classroom_ids).select_related('classroom')

    def get_user_chat_rooms(self):
        classroom_ids = self.get_user_classrooms().values_list('id', flat=True)
        rooms = ChatRoom.objects.filter(
            Q(classroom_id__in=classroom_ids) | Q(classroom__isnull=True, name='Tutor Announcements'),
            is_active=True, room_type__in=['group', 'voice'],
        ).select_related('classroom')
        if self.request.user.is_staff or self.request.user.is_superuser:
            return rooms.distinct()
        return rooms.distinct()

    def mark_attendance(self, classrooms):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return
        today = timezone.localdate()
        for classroom in classrooms:
            AttendanceRecord.objects.get_or_create(
                classroom=classroom,
                student=self.request.user,
                attended_on=today,
                defaults={'was_present': True},
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classrooms = self.get_user_classrooms()
        assignments = self.get_user_assignments()
        classroom_ids = classrooms.values_list('id', flat=True)
        chat_rooms = self.get_user_chat_rooms()
        self.mark_attendance(classrooms)
        context['classrooms'] = classrooms[:8]
        context['available_classrooms'] = Classroom.objects.filter(is_active=True).exclude(
            memberships__student=self.request.user,
        ).select_related('trainer', 'learning_path')[:4]
        context['assignments'] = assignments[:8]
        context['materials'] = LearningMaterial.objects.filter(
            Q(classroom_id__in=classroom_ids) | Q(classroom__isnull=True, learning_path__classrooms__id__in=classroom_ids)
        ).select_related('classroom', 'learning_path').distinct()[:8]
        context['announcements'] = Announcement.objects.filter(
            Q(classroom_id__in=classroom_ids) | Q(classroom__isnull=True)
        ).select_related('classroom')[:6]
        context['live_sessions'] = LiveSession.objects.filter(
            Q(classroom_id__in=classroom_ids) | Q(classroom__isnull=True),
            is_open=True,
        ).select_related('classroom')[:6]
        context['chat_rooms'] = chat_rooms[:6]
        context['chat_messages'] = ChatMessage.objects.filter(room__in=chat_rooms).select_related('room', 'sender')[:8]
        context['submissions'] = Submission.objects.filter(
            student=self.request.user,
            assignment__classroom_id__in=classroom_ids,
        ).select_related('assignment', 'assignment__classroom')[:8]
        context['attendance_count'] = AttendanceRecord.objects.filter(
            student=self.request.user,
            classroom_id__in=classroom_ids,
            was_present=True,
        ).count()
        context['join_form'] = kwargs.get('join_form') or JoinClassForm()
        context['create_form'] = kwargs.get('create_form') or CreateClassroomForm()
        context['submission_form'] = kwargs.get('submission_form') or AssignmentSubmissionForm(assignments=assignments)
        context['chat_form'] = kwargs.get('chat_form') or ChatMessageForm(rooms=chat_rooms)
        context['can_manage_classrooms'] = self.user_can_manage()
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('form_action')
        if action == 'join_class':
            return self.join_class(request)
        if action == 'create_classroom':
            return self.create_classroom(request)
        if action == 'submit_assignment':
            return self.submit_assignment(request)
        if action == 'send_chat_message':
            return self.send_chat_message(request)
        messages.error(request, 'Choose a classroom action and try again.')
        return redirect('academy:classroom')

    def join_class(self, request):
        form = JoinClassForm(request.POST)
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(join_form=form))
        classroom = Classroom.objects.filter(class_code__iexact=form.cleaned_data['class_code'], is_active=True).first()
        if not classroom:
            form.add_error('class_code', 'No active classroom uses that code.')
            return self.render_to_response(self.get_context_data(join_form=form))
        membership, created = ClassMembership.objects.get_or_create(classroom=classroom, student=request.user)
        chat_room, _created = ChatRoom.objects.get_or_create(
            classroom=classroom,
            name=f'{classroom.name} Stream',
            defaults={'room_type': 'group', 'is_active': True},
        )
        chat_room.participants.add(request.user)
        AttendanceRecord.objects.get_or_create(
            classroom=classroom,
            student=request.user,
            attended_on=timezone.localdate(),
            defaults={'was_present': True},
        )
        if created:
            messages.success(request, f'You joined {classroom.name}.')
        else:
            messages.info(request, f'You are already enrolled in {classroom.name}.')
        return redirect('academy:classroom')

    def create_classroom(self, request):
        if not self.user_can_manage():
            messages.error(request, 'Only approved trainers and staff can create classrooms.')
            return redirect('academy:classroom')
        form = CreateClassroomForm(request.POST)
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(create_form=form))
        classroom = form.save(commit=False)
        classroom.trainer = getattr(request.user, 'trainer_profile', None)
        classroom.is_active = True
        classroom.save()
        chat_room, _created = ChatRoom.objects.get_or_create(
            classroom=classroom,
            name=f'{classroom.name} Stream',
            defaults={'room_type': 'group', 'is_active': True},
        )
        chat_room.participants.add(request.user)
        if classroom.meeting_link:
            LiveSession.objects.get_or_create(
                classroom=classroom,
                title=f'{classroom.name} Live Room',
                defaults={
                    'session_type': 'video',
                    'meeting_url': classroom.meeting_link,
                    'agenda': 'Live lessons, screen sharing, questions, and trainer feedback.',
                    'scheduled_for': timezone.now(),
                    'is_open': True,
                },
            )
        messages.success(request, f'{classroom.name} is ready. Share class code {classroom.class_code} with students.')
        return redirect('academy:classroom')

    def submit_assignment(self, request):
        assignments = self.get_user_assignments()
        form = AssignmentSubmissionForm(request.POST, request.FILES, assignments=assignments)
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(submission_form=form))
        assignment = form.cleaned_data['assignment']
        defaults = {'notes': form.cleaned_data.get('notes', '')}
        if form.cleaned_data.get('file'):
            defaults['file'] = form.cleaned_data['file']
        Submission.objects.update_or_create(
            assignment=assignment,
            student=request.user,
            defaults=defaults,
        )
        messages.success(request, f'Submission received for {assignment.title}.')
        return redirect('academy:classroom')

    def send_chat_message(self, request):
        rooms = self.get_user_chat_rooms()
        form = ChatMessageForm(request.POST, rooms=rooms)
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(chat_form=form))
        message = form.save(commit=False)
        message.sender = request.user
        message.sender_name = request.user.get_full_name() or request.user.username
        message.save()
        form.cleaned_data['room'].participants.add(request.user)
        messages.success(request, 'Your message was posted to the class chat.')
        return redirect('academy:classroom')


def mentor_answer(question):
    question_lower = question.lower()
    if 'python' in question_lower:
        return 'Start with Python fundamentals, then build three mini projects: a grade calculator, a file organizer, and a simple Django app. Practice daily and explain each concept in your own words.'
    if 'ai' in question_lower or 'machine learning' in question_lower:
        return 'Begin with Python, data basics, and responsible AI. Your first AI project can classify simple data, summarize text, or recommend learning paths. Always document the data, assumptions, and limitations.'
    if 'career' in question_lower or 'job' in question_lower or 'internship' in question_lower:
        return 'Build a focused portfolio: one web app, one data or automation project, and one teamwork story. Add a clear resume, GitHub links, and short case studies that explain the problem, process, and result.'
    if 'project' in question_lower:
        return 'Choose a project that solves a real problem near you. Good beginner ideas include a school club website, event registration system, study planner, expense tracker, or community resource directory.'
    return 'Break the topic into fundamentals, practice tasks, and a portfolio project. KodaGrid Mentor AI recommends learning one concept, building one small example, then teaching it back before moving on.'


class MentorAIView(FormView):
    template_name = 'academy/ai_mentor.html'
    form_class = MentorAIForm
    success_url = reverse_lazy('academy:ai_mentor')

    def form_valid(self, form):
        interaction = form.save(commit=False)
        interaction.answer = mentor_answer(interaction.question)
        interaction.save()
        self.request.session['mentor_answer'] = interaction.answer
        self.request.session['mentor_question'] = interaction.question
        messages.success(self.request, 'KodaGrid Mentor AI prepared a learning recommendation.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentor_answer'] = self.request.session.pop('mentor_answer', '')
        context['mentor_question'] = self.request.session.pop('mentor_question', '')
        context['recent_interactions'] = MentorAIInteraction.objects.all()[:4]
        return context


class CertificateVerifyView(DetailView):
    model = Certificate
    template_name = 'academy/certificate_verify.html'
    context_object_name = 'certificate'
    slug_field = 'verification_code'
    slug_url_kwarg = 'code'


class LessonView(TemplateView):
    template_name = 'academy/lesson.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path    = get_object_or_404(LearningPath, slug=kwargs['slug'])
        lessons = list(path.lessons.all().order_by('order'))

        order   = int(kwargs.get('order', 1))
        current = next((l for l in lessons if l.order == order), lessons[0] if lessons else None)
        if not current and lessons:
            current = lessons[0]

        current_idx = lessons.index(current) if current in lessons else 0

        context['path']           = path
        context['lessons']        = lessons
        context['lesson']         = current
        context['prev_lesson']    = lessons[current_idx - 1] if current_idx > 0 else None
        context['next_lesson']    = lessons[current_idx + 1] if current_idx < len(lessons) - 1 else None
        context['lesson_num']     = current_idx + 1
        context['total_lessons']  = len(lessons)
        context['progress_pct']   = int(((current_idx) / max(len(lessons), 1)) * 100)
        context['completed_pct']  = int(((current_idx + 1) / max(len(lessons), 1)) * 100)

        # Detect primary language for Try it editor
        title_lower = path.title.lower()
        if 'python' in title_lower:          context['editor_lang'] = 'python'
        elif 'html' in title_lower:          context['editor_lang'] = 'html'
        elif 'css' in title_lower:           context['editor_lang'] = 'css'
        elif 'javascript' in title_lower or 'js' in title_lower: context['editor_lang'] = 'javascript'
        elif 'java ' in title_lower:         context['editor_lang'] = 'java'
        elif 'sql' in title_lower:           context['editor_lang'] = 'sql'
        elif 'scratch' in title_lower:       context['editor_lang'] = 'scratch'
        elif 'c++' in title_lower or 'cpp' in title_lower: context['editor_lang'] = 'cpp'
        else:                                context['editor_lang'] = 'python'
        return context


class TryItView(TemplateView):
    template_name = 'academy/tryit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lang'] = self.request.GET.get('lang', 'html')
        return context


class TechGirlView(TemplateView):
    template_name = 'academy/techgirl.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from gallery.models import GalleryImage
        girls_images = GalleryImage.objects.filter(
            Q(suggested_placement__icontains='Girls') |
            Q(detected_subject__icontains='girl') |
            Q(detected_subject__icontains='women') |
            Q(caption__icontains='code') |
            Q(caption__icontains='tech')
        ).exclude(image='').exclude(image__isnull=True)[:12]
        if girls_images.count() < 4:
            girls_images = GalleryImage.objects.exclude(image='').exclude(image__isnull=True)[:12]
        context['girls_images'] = girls_images
        context['role_models'] = [
            {'name': 'Ada Lovelace',       'role': 'First Computer Programmer', 'fact': 'Wrote the first algorithm in 1843 — before computers even existed.'},
            {'name': 'Grace Hopper',       'role': 'Invented the Compiler',     'fact': 'Made programming accessible to humans by translating code into machine language.'},
            {'name': 'Radia Perlman',      'role': 'Mother of the Internet',    'fact': 'Invented the Spanning Tree Protocol that makes modern networks possible.'},
            {'name': 'Katherine Johnson',  'role': 'NASA Mathematician',        'fact': 'Calculated trajectories for the Apollo 11 mission to the Moon.'},
            {'name': 'Timnit Gebru',       'role': 'AI Ethics Researcher',      'fact': 'Pioneering work exposing bias in facial recognition systems.'},
            {'name': 'Reshma Saujani',     'role': 'Girls Who Code Founder',    'fact': 'Has taught over 500,000 girls to code across the world.'},
        ]
        context['programs'] = [
            {'icon': 'laptop',    'title': 'She Codes',          'desc': 'Beginner-friendly Python, web, and app development tailored for girls aged 12–18.',  'course_slug': 'python-programming'},
            {'icon': 'cpu',       'title': 'Robotics for Girls', 'desc': 'Build and program robots using Arduino and LEGO. No experience required.',            'course_slug': 'robotics-physical-computing'},
            {'icon': 'bar-chart', 'title': 'Data She Dares',     'desc': 'Data science, AI, and visualization projects solving real community problems.',        'course_slug': 'data-science'},
            {'icon': 'palette',   'title': 'Creative Tech',      'desc': 'Blend art, design, and code — build websites, games, and digital experiences.',       'course_slug': 'ui-ux-design'},
            {'icon': 'rocket',    'title': 'Future Founders',    'desc': 'Launch a tech startup: from idea validation to your first product demo.',              'course_slug': 'digital-marketing'},
            {'icon': 'trophy',    'title': 'Hackathon Squad',    'desc': 'Join all-girls teams competing in national and international coding challenges.',      'course_slug': 'web-development'},
        ]
        context['scholarships'] = [
            {'org': 'Google Women Techmakers', 'value': 'Full scholarship + mentorship', 'region': 'Global'},
            {'org': 'Andela Learning Community', 'value': 'Free coding bootcamp', 'region': 'Africa'},
            {'org': 'Girls Who Code',           'value': 'Free summer immersion', 'region': 'USA / Virtual'},
            {'org': 'AnitaB.org Grace Hopper',  'value': 'Conference + networking', 'region': 'Global'},
        ]
        return context


class TechBoyView(TemplateView):
    template_name = 'academy/techboy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from gallery.models import GalleryImage
        from django.db.models import Q
        boy_images = GalleryImage.objects.exclude(image='').exclude(image__isnull=True).exclude(
            Q(detected_subject__icontains='girl') |
            Q(detected_subject__icontains='woman') |
            Q(detected_subject__icontains='female')
        )[:12]
        if boy_images.count() < 4:
            boy_images = GalleryImage.objects.exclude(image='').exclude(image__isnull=True)[:12]
        context['boy_images'] = boy_images
        context['role_models'] = [
            {'name': 'Linus Torvalds',   'role': 'Creator of Linux & Git',      'fact': 'Started Linux at age 21 in a college dorm room. Now powers 97% of the internet.'},
            {'name': 'Elon Musk',        'role': 'Tesla, SpaceX, xAI Founder',  'fact': 'Taught himself programming at 9. Sold his first game at 12 for $500.'},
            {'name': 'Mark Zuckerberg',  'role': 'Meta Founder',                'fact': 'Built Facebook at 19 while studying at Harvard.'},
            {'name': 'Karim Aboutaleb',  'role': 'African Tech Entrepreneur',   'fact': 'Built one of Africa\'s fastest-growing fintech platforms from Nairobi.'},
            {'name': 'Andile Ngcaba',    'role': 'Africa Tech Pioneer',         'fact': 'Helped bring the internet to millions of Africans through infrastructure investment.'},
            {'name': 'Turing (Alan)',    'role': 'Father of Computer Science',  'fact': 'Cracked Nazi codes in WWII and laid the foundations for all modern AI.'},
        ]
        context['programs'] = [
            {'icon': 'file-earmark-code', 'title': 'Code Warriors',   'desc': 'Python, C++, and algorithms. Build games, automations, and command-line tools.',    'course_slug': 'python-programming'},
            {'icon': 'cpu-fill',          'title': 'Robotics Lab',    'desc': 'Wire up Arduino, program sensors, and build robots that solve real problems.',       'course_slug': 'robotics-physical-computing'},
            {'icon': 'controller',        'title': 'Game Dev Studio', 'desc': 'Build 2D games with Python (Pygame) or JavaScript (Phaser). Ship your first game.', 'course_slug': 'web-development'},
            {'icon': 'shield-lock',       'title': 'Cyber Defenders', 'desc': 'Ethical hacking, network security, and CTF challenges for the bold.',                'course_slug': 'cybersecurity-foundations'},
            {'icon': 'cloud-upload',      'title': 'Cloud & DevOps',  'desc': 'Deploy apps to AWS, set up CI/CD pipelines, and manage Linux servers.',              'course_slug': 'cloud-computing'},
            {'icon': 'trophy-fill',       'title': 'Compete & Win',   'desc': 'ICPC, hackathons, Codeforces, and LeetCode coaching to reach the top.',              'course_slug': 'python-programming'},
        ]
        context['challenges'] = [
            {'title': '30-Day Python Sprint', 'difficulty': 'Beginner', 'prize': 'Certificate + LinkedIn badge'},
            {'title': 'Build a CLI App',      'difficulty': 'Intermediate', 'prize': 'Feature in Academy Showcase'},
            {'title': 'Cybersecurity CTF',    'difficulty': 'Advanced', 'prize': 'Cash prize + Internship fast-track'},
            {'title': 'Robotics Showdown',    'difficulty': 'All levels', 'prize': 'Kit giveaway + trophy'},
        ]
        return context


class AssessmentView(TemplateView):
    template_name = 'academy/assessment.html'

    QUESTIONS = [
        # (id, category, question, options, correct_index, points)
        ('q1',  'logic',   'If all Bloops are Razzies and all Razzies are Lazzies, are all Bloops definitely Lazzies?',
         ['Yes', 'No', 'Cannot be determined', 'Only sometimes'], 0, 5),
        ('q2',  'logic',   'A train travels 60 km/h for 2 hours. How far does it travel?',
         ['100 km', '120 km', '130 km', '90 km'], 1, 5),
        ('q3',  'logic',   'Which number comes next? 2, 4, 8, 16, ___',
         ['24', '32', '20', '18'], 1, 5),
        ('q4',  'math',    'What is 15% of 200?',
         ['25', '30', '35', '20'], 1, 5),
        ('q5',  'math',    'If x = 3 and y = 4, what is x² + y²?',
         ['25', '14', '49', '12'], 0, 5),
        ('q6',  'math',    'A rectangle has length 8 and width 5. What is its area?',
         ['13', '26', '40', '45'], 2, 5),
        ('q7',  'tech',    'What does HTML stand for?',
         ['HyperText Markup Language', 'HighText Machine Language', 'Home Tool Markup Language', 'Hyperlink Text Method Language'], 0, 5),
        ('q8',  'tech',    'Which symbol starts a comment in Python?',
         ['//', '#', '--', '/*'], 1, 5),
        ('q9',  'tech',    'What is the output of: print(2 ** 3) in Python?',
         ['6', '8', '9', '5'], 1, 5),
        ('q10', 'tech',    'Which of these is NOT a programming language?',
         ['Rust', 'Kotlin', 'HTML', 'Swift'], 2, 5),
        ('q11', 'problem', 'You need to find the tallest person in a list of 100 people. What is the minimum number of comparisons needed?',
         ['50', '99', '100', '10'], 1, 5),
        ('q12', 'problem', 'A bug keeps crashing your app every Friday at midnight. What is the BEST first step?',
         ['Restart the server', 'Check the logs for that time', 'Rewrite the whole app', 'Ignore it'], 1, 5),
        ('q13', 'style',   'How do you prefer to learn something new?',
         ['Watching videos / diagrams', 'Reading documentation', 'Building projects immediately', 'Listening to explanations'], None, 0),
        ('q14', 'style',   'How old are you?',
         ['Under 12', '12–15', '16–20', '21+'], None, 0),
        ('q15', 'style',   'What excites you most about technology?',
         ['Building websites & apps', 'Data, AI & machine learning', 'Games & creative projects', 'Security & problem solving'], None, 0),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.QUESTIONS
        context['total_questions'] = len(self.QUESTIONS)
        existing = None
        if self.request.user.is_authenticated:
            existing = SkillAssessment.objects.filter(user=self.request.user).first()
        elif self.request.session.session_key:
            existing = SkillAssessment.objects.filter(session_key=self.request.session.session_key).first()
        context['existing_assessment'] = existing
        return context

    def post(self, request, *args, **kwargs):
        from django.utils import timezone
        answers = {}
        score = 0
        strengths = []
        interests = []

        category_scores = {'logic': 0, 'math': 0, 'tech': 0, 'problem': 0}
        category_max    = {'logic': 15, 'math': 15, 'tech': 20, 'problem': 10}

        for q_id, category, question, options, correct_idx, points in self.QUESTIONS:
            user_answer = request.POST.get(q_id)
            answers[q_id] = user_answer
            if correct_idx is not None and user_answer is not None:
                try:
                    if int(user_answer) == correct_idx:
                        score += points
                        category_scores[category] = category_scores.get(category, 0) + points
                except (ValueError, TypeError):
                    pass

        # Derive strengths
        for cat, cat_score in category_scores.items():
            pct = (cat_score / category_max.get(cat, 10)) * 100 if category_max.get(cat) else 0
            if pct >= 70:
                strengths.append(cat.title())

        # Age group
        age_ans = answers.get('q14', '1')
        try:
            age_idx = int(age_ans)
            age_map = {0: 'Under 12', 1: '12–15', 2: '16–20', 3: '21+'}
            age_group = age_map.get(age_idx, '16–20')
        except (ValueError, TypeError):
            age_group = '16–20'

        # Learning style
        style_ans = answers.get('q13', '2')
        try:
            style_map = {0: 'visual', 1: 'reading', 2: 'kinesthetic', 3: 'auditory'}
            learning_style = style_map.get(int(style_ans), 'kinesthetic')
        except (ValueError, TypeError):
            learning_style = 'kinesthetic'

        # Interests
        interest_ans = answers.get('q15', '0')
        try:
            interest_map = {0: 'Web Dev', 1: 'AI & Data', 2: 'Games', 3: 'Security'}
            interests = [interest_map.get(int(interest_ans), 'Web Dev')]
        except (ValueError, TypeError):
            interests = ['Web Dev']

        # Skill level & recommended paths
        max_score = 60
        pct = (score / max_score) * 100

        if age_group == 'Under 12' or pct < 20:
            skill_level = 'explorer'
            recommended_paths = ['Scratch for Kids', 'HTML Basics', 'Robotics Intro']
            recommended_books = [
                {'title': 'Hello Ruby', 'author': 'Linda Liukas', 'why': 'Perfect intro to programming for children through stories.'},
                {'title': 'Coding Games in Scratch', 'author': 'Jon Woodcock', 'why': 'Visual block-based coding through fun games.'},
                {'title': 'How to Be a Coder', 'author': 'Kiki Prottsman', 'why': 'Step-by-step coding concepts designed for kids.'},
            ]
        elif pct < 40:
            skill_level = 'beginner'
            recommended_paths = ['Python Basics', 'HTML & CSS', 'JavaScript Intro']
            recommended_books = [
                {'title': 'Python Crash Course', 'author': 'Eric Matthes', 'why': 'The most beginner-friendly Python book available.'},
                {'title': 'Eloquent JavaScript', 'author': 'Marijn Haverbeke', 'why': 'From zero to real JS projects, free online.'},
                {'title': 'HTML & CSS: Design and Build Websites', 'author': 'Jon Duckett', 'why': 'Beautiful visual guide to web fundamentals.'},
            ]
        elif pct < 65:
            skill_level = 'intermediate'
            recommended_paths = ['Django Web Dev', 'React', 'Python Data Science'] if 'AI & Data' in interests else ['Django Web Dev', 'React', 'JavaScript Frameworks']
            recommended_books = [
                {'title': 'Clean Code', 'author': 'Robert C. Martin', 'why': 'Learn to write code that lasts and teams love to read.'},
                {'title': 'Django for Beginners', 'author': 'William S. Vincent', 'why': 'Project-based Django book from scratch to deployment.'},
                {'title': 'You Don\'t Know JS', 'author': 'Kyle Simpson', 'why': 'Deepens JS understanding beyond surface-level tutorials.'},
            ]
        elif pct < 85:
            skill_level = 'advanced'
            recommended_paths = ['Machine Learning', 'Cloud AWS', 'System Design']
            recommended_books = [
                {'title': 'Designing Data-Intensive Applications', 'author': 'Martin Kleppmann', 'why': 'The definitive book on scalable system design.'},
                {'title': 'The Pragmatic Programmer', 'author': 'Hunt & Thomas', 'why': 'Timeless advice for writing professional software.'},
                {'title': 'Hands-On Machine Learning', 'author': 'Aurélien Géron', 'why': 'Industry-standard ML with scikit-learn and TensorFlow.'},
            ]
        else:
            skill_level = 'expert'
            recommended_paths = ['Generative AI', 'Cybersecurity', 'Cloud Architecture']
            recommended_books = [
                {'title': 'The Art of Computer Programming', 'author': 'Donald Knuth', 'why': 'The bible of algorithms — for those who want mastery.'},
                {'title': 'SICP (Structure and Interpretation of Computer Programs)', 'author': 'Abelson & Sussman', 'why': 'Legendary MIT textbook that will reshape how you think.'},
                {'title': 'Deep Learning', 'author': 'Goodfellow, Bengio, Courville', 'why': 'Authoritative reference for serious AI practitioners.'},
            ]

        # Save assessment
        if not request.session.session_key:
            request.session.create()

        assessment_data = dict(
            skill_level=skill_level,
            iq_score=score,
            age_group=age_group,
            learning_style=learning_style,
            strengths=strengths or ['Problem Solving'],
            interests=interests,
            recommended_paths=recommended_paths,
            recommended_books=recommended_books,
            answers=answers,
            completed_at=timezone.now(),
        )

        if request.user.is_authenticated:
            assessment, _ = SkillAssessment.objects.update_or_create(
                user=request.user, defaults=assessment_data
            )
        else:
            assessment, _ = SkillAssessment.objects.update_or_create(
                session_key=request.session.session_key, defaults=assessment_data
            )

        request.session['assessment_id'] = assessment.pk
        return redirect(reverse_lazy('academy:assessment_result'))


class AssessmentResultView(TemplateView):
    template_name = 'academy/assessment_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assessment = None
        if self.request.user.is_authenticated:
            assessment = SkillAssessment.objects.filter(user=self.request.user).first()
        if not assessment:
            pk = self.request.session.get('assessment_id')
            if pk:
                assessment = SkillAssessment.objects.filter(pk=pk).first()
        context['assessment'] = assessment

        # Extra recommendations per path
        path_detail = {
            'Scratch for Kids':      {'icon': '🐱', 'time': '4 weeks', 'url': '/learn/'},
            'HTML Basics':           {'icon': '🌐', 'time': '3 weeks', 'url': '/learn/'},
            'Robotics Intro':        {'icon': '🤖', 'time': '6 weeks', 'url': '/robotics/'},
            'Python Basics':         {'icon': '🐍', 'time': '6 weeks', 'url': '/learn/'},
            'HTML & CSS':            {'icon': '🎨', 'time': '4 weeks', 'url': '/learn/'},
            'JavaScript Intro':      {'icon': '⚡', 'time': '5 weeks', 'url': '/learn/'},
            'Django Web Dev':        {'icon': '🦄', 'time': '8 weeks', 'url': '/learn/'},
            'React':                 {'icon': '⚛️', 'time': '6 weeks', 'url': '/learn/'},
            'Python Data Science':   {'icon': '📊', 'time': '8 weeks', 'url': '/learn/'},
            'JavaScript Frameworks': {'icon': '🔧', 'time': '6 weeks', 'url': '/learn/'},
            'Machine Learning':      {'icon': '🧠', 'time': '10 weeks', 'url': '/learn/'},
            'Cloud AWS':             {'icon': '☁️', 'time': '8 weeks', 'url': '/learn/'},
            'System Design':         {'icon': '🏗️', 'time': '6 weeks', 'url': '/learn/'},
            'Generative AI':         {'icon': '✨', 'time': '8 weeks', 'url': '/learn/'},
            'Cybersecurity':         {'icon': '🔐', 'time': '10 weeks', 'url': '/learn/'},
            'Cloud Architecture':    {'icon': '🌩️', 'time': '8 weeks', 'url': '/learn/'},
        }
        context['path_detail'] = path_detail
        context['revision_tips'] = {
            'visual':      ['Draw diagrams of what you learn', 'Use Figma to map concepts', 'Watch YouTube coding walkthroughs'],
            'reading':     ['Keep a code journal', 'Read the official docs first', 'Take typed notes while coding'],
            'kinesthetic': ['Build a project on day one', 'Clone a real app and add features', 'Do exercises before reading theory'],
            'auditory':    ['Listen to Syntax.fm podcast', 'Use voice-to-text for notes', 'Find a study partner to explain concepts to'],
        }
        return context


class RoboticsView(TemplateView):
    template_name = 'academy/robotics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kits'] = RoboticsKit.objects.all()
        context['featured_kits'] = RoboticsKit.objects.filter(is_featured=True)[:4]
        context['age_groups'] = [
            ('kids',         '🐣 Ages 6–10',  'Scratch-programmable, no soldering, fun block coding'),
            ('beginner',     '🌱 Ages 11–14', 'Arduino starters, sensors, simple circuits'),
            ('intermediate', '⚡ Ages 14+',   'Raspberry Pi, motor drivers, OpenCV'),
            ('advanced',     '🚀 Advanced',   'ROS, computer vision, autonomous navigation'),
        ]
        return context


class VideoCallView(LoginRequiredMixin, TemplateView):
    template_name = 'academy/video_call.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_code = kwargs.get('room_code', 'general')
        classroom = Classroom.objects.filter(class_code__iexact=room_code, is_active=True).first()
        private_room = ChatRoom.objects.filter(call_code=room_code, room_type='private', is_active=True).first()
        if private_room and not private_room.participants.filter(pk=self.request.user.pk).exists():
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        if classroom and not (classroom.memberships.filter(student=self.request.user).exists()
                              or self.request.user.is_staff or self.request.user.is_superuser
                              or TrainerProfile.objects.filter(user=self.request.user, is_approved=True).exists()):
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        if not classroom and not private_room:
            from django.http import Http404
            raise Http404
        classroom_chat = None
        if classroom:
            classroom_chat, _ = ChatRoom.objects.get_or_create(
                classroom=classroom, name=f'{classroom.name} Stream',
                defaults={'room_type': 'group', 'is_active': True},
            )
            member_ids = list(classroom.memberships.values_list('student_id', flat=True))
            if classroom.trainer_id and classroom.trainer.user_id:
                member_ids.append(classroom.trainer.user_id)
            classroom_chat.participants.add(*member_ids)
        context['room_code'] = room_code
        context['classroom'] = classroom
        context['chat_room_id'] = private_room.pk if private_room else (classroom_chat.pk if classroom_chat else '')
        context['chat_user_role'] = 'trainer' if _chat_can_announce(self.request.user) else 'student'
        context['jitsi_room'] = f'KodaGrid-{private_room.call_code}' if private_room else f'KodaGrid-{classroom.class_code}'
        context['back_url'] = self.request.META.get('HTTP_REFERER', '/accounts/profile/')
        return context


class GamesView(TemplateView):
    template_name = 'academy/games.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leaderboard'] = [
            {'rank': 1, 'name': 'Amara O.',   'score': 2840, 'badge': '🥇'},
            {'rank': 2, 'name': 'Brian M.',   'score': 2410, 'badge': '🥈'},
            {'rank': 3, 'name': 'Grace N.',   'score': 1980, 'badge': '🥉'},
            {'rank': 4, 'name': 'Kofi A.',    'score': 1750, 'badge': '⭐'},
            {'rank': 5, 'name': 'Zara K.',    'score': 1620, 'badge': '⭐'},
        ]
        return context


class LiveChatView(LoginRequiredMixin, TemplateView):
    template_name = 'academy/live_chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = ChatRoom.objects.filter(room_type='group', name='Tutor Announcements', is_active=True)[:1]
        context['featured_room'] = context['rooms'].first() if context['rooms'] else None
        context['trainers_online'] = TrainerProfile.objects.filter(is_approved=True, user__isnull=False).select_related('user')[:30]
        context['chat_user_role'] = 'trainer' if _chat_can_announce(self.request.user) else 'student'
        return context


def _chat_can_announce(user):
    return user.is_staff or user.is_superuser or TrainerProfile.objects.filter(user=user, is_approved=True).exists()


@login_required
@ensure_csrf_cookie
@require_http_methods(['GET', 'POST'])
def chat_api(request):
    """Authenticated polling chat. Private rooms are visible only to their two members."""
    if request.method == 'GET':
        room_id = request.GET.get('room')
        if not room_id:
            announcements, _ = ChatRoom.objects.get_or_create(
                room_type='group', name='Tutor Announcements',
                defaults={'is_active': True},
            )
            rooms = ChatRoom.objects.filter(is_active=True, room_type='private', participants=request.user).distinct()
            conversations = []
            for room in rooms:
                peer = room.participants.exclude(pk=request.user.pk).first()
                if peer:
                    conversations.append({'id': room.pk, 'name': peer.get_full_name() or peer.username, 'user_id': peer.pk, 'type': 'private'})
            User = type(request.user)
            query = request.GET.get('q', '').strip()[:80]
            users = User.objects.filter(is_active=True).exclude(pk=request.user.pk)
            if query:
                users = users.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
            users = users.order_by('first_name', 'last_name', 'username')[:30]
            directory = [{'id': u.pk, 'name': u.get_full_name() or u.username,
                          'role': 'trainer' if _chat_can_announce(u) else 'student'} for u in users]
            return JsonResponse({'conversations': conversations, 'announcements': announcements.pk,
                                 'can_announce': _chat_can_announce(request.user), 'users': directory})
        room = get_object_or_404(ChatRoom, pk=room_id, is_active=True)
        allowed = room.participants.filter(pk=request.user.pk).exists()
        if room.room_type == 'group' and room.name == 'Tutor Announcements':
            allowed = True
        if not allowed:
            return JsonResponse({'error': 'Conversation not found.'}, status=404)
        after = request.GET.get('after', '0')
        try:
            after = max(0, int(after))
        except ValueError:
            after = 0
        messages_qs = list(room.messages.filter(pk__gt=after).select_related('sender').order_by('created_at')[:100])
        trainer_ids = set(TrainerProfile.objects.filter(
            user_id__in=[m.sender_id for m in messages_qs if m.sender_id], is_approved=True,
        ).values_list('user_id', flat=True))
        return JsonResponse({'messages': [{'id': m.pk, 'text': m.body, 'user': m.sender_name,
            'time': m.created_at.isoformat(), 'mine': m.sender_id == request.user.pk,
            'role': 'trainer' if m.sender_id in trainer_ids else 'student'} for m in messages_qs]})

    try:
        payload = json.loads(request.body or '{}')
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid request.'}, status=400)
    action = payload.get('action')
    if action == 'start':
        try:
            peer = get_object_or_404(type(request.user), pk=int(payload.get('user_id')))
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Choose a valid account.'}, status=400)
        if peer.pk == request.user.pk or not peer.is_active:
            return JsonResponse({'error': 'Choose another active account.'}, status=400)
        candidates = ChatRoom.objects.filter(room_type='private', is_active=True, participants=request.user).filter(participants=peer)
        room = next((r for r in candidates if r.participants.count() == 2), None)
        if not room:
            room = ChatRoom.objects.create(name='Private conversation', room_type='private')
            room.participants.add(request.user, peer)
        return JsonResponse({'id': room.pk, 'name': peer.get_full_name() or peer.username})
    room = get_object_or_404(ChatRoom, pk=payload.get('room'), is_active=True)
    is_announcement = room.room_type == 'group' and room.name == 'Tutor Announcements'
    if not (room.participants.filter(pk=request.user.pk).exists() or is_announcement):
        return JsonResponse({'error': 'Conversation not found.'}, status=404)
    if action == 'invite':
        if room.room_type != 'private':
            return JsonResponse({'error': 'Calls are available in private conversations.'}, status=400)
        call_url = request.build_absolute_uri(reverse_lazy('academy:video_call', kwargs={'room_code': str(room.call_code)}))
        ChatMessage.objects.create(room=room, sender=request.user,
            sender_name=request.user.get_full_name() or request.user.username,
            body=f'Call invitation: {call_url}')
        return JsonResponse({'url': call_url}, status=201)
    if is_announcement and not _chat_can_announce(request.user):
        return JsonResponse({'error': 'Only tutors and mentors can post announcements.'}, status=403)
    body = str(payload.get('text', '')).strip()
    if not body or len(body) > 1000:
        return JsonResponse({'error': 'Messages must contain 1 to 1000 characters.'}, status=400)
    message = ChatMessage.objects.create(room=room, sender=request.user,
        sender_name=request.user.get_full_name() or request.user.username, body=body)
    if room.room_type == 'private':
        room.participants.add(request.user)
    return JsonResponse({'id': message.pk}, status=201)
