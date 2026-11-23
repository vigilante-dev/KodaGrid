from django.contrib import admin

from .models import (
    Announcement,
    Assignment,
    AttendanceRecord,
    Certificate,
    ChatMessage,
    ChatRoom,
    ClassMembership,
    Classroom,
    CommunityChallenge,
    GameScore,
    FeePlan,
    ForumReply,
    ForumTopic,
    JobOpportunity,
    LearningMaterial,
    LearningPath,
    Lesson,
    LiveSession,
    MentorAIInteraction,
    MentorshipBooking,
    Resource,
    Submission,
    TrainerApplication,
    TrainerProfile,
)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ('order', 'title', 'estimated_minutes')


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'duration', 'is_featured')
    list_filter = ('category', 'level', 'is_featured')
    search_fields = ('title', 'summary', 'skill_stack')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'learning_path', 'order', 'estimated_minutes')
    list_filter = ('learning_path__category', 'learning_path')
    search_fields = ('title', 'objective', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'headline', 'email', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('name', 'email', 'skills', 'courses_taught')


@admin.register(TrainerApplication)
class TrainerApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'expertise', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'expertise', 'bio')


@admin.register(MentorshipBooking)
class MentorshipBookingAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'trainer', 'topic', 'preferred_time', 'status')
    list_filter = ('status', 'preferred_time')
    search_fields = ('student_name', 'email', 'topic')


class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0


class MaterialInline(admin.TabularInline):
    model = LearningMaterial
    extra = 0


class AnnouncementInline(admin.TabularInline):
    model = Announcement
    extra = 0


class LiveSessionInline(admin.TabularInline):
    model = LiveSession
    extra = 0


class ChatRoomInline(admin.TabularInline):
    model = ChatRoom
    extra = 0


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_code', 'trainer', 'course', 'learning_path', 'start_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'course')
    autocomplete_fields = ('course',)
    search_fields = ('name', 'class_code', 'description')
    inlines = [AssignmentInline, MaterialInline, AnnouncementInline, LiveSessionInline, ChatRoomInline]


@admin.register(ClassMembership)
class ClassMembershipAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'student', 'progress_percent', 'joined_at')
    list_filter = ('classroom', 'joined_at')
    search_fields = ('classroom__name', 'student__username', 'student__email')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'classroom', 'due_date', 'max_score')
    list_filter = ('classroom', 'due_date')
    search_fields = ('title', 'instructions')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'grade', 'submitted_at')
    list_filter = ('assignment', 'submitted_at')
    search_fields = ('assignment__title', 'student__username', 'notes')


@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'classroom', 'learning_path', 'created_at')
    list_filter = ('material_type', 'created_at')
    search_fields = ('title', 'description')


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'student', 'attended_on', 'was_present')
    list_filter = ('classroom', 'was_present', 'attended_on')
    search_fields = ('classroom__name', 'student__username')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'classroom', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'message')


@admin.register(LiveSession)
class LiveSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'classroom', 'session_type', 'scheduled_for', 'is_open')
    list_filter = ('session_type', 'is_open', 'scheduled_for')
    search_fields = ('title', 'agenda', 'meeting_url', 'classroom__name')


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'classroom', 'room_type', 'is_active')
    list_filter = ('room_type', 'is_active')
    search_fields = ('name', 'classroom__name')
    filter_horizontal = ('participants',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender_name', 'created_at')
    list_filter = ('created_at', 'room')
    search_fields = ('sender_name', 'body', 'room__name')


@admin.register(FeePlan)
class FeePlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'monthly_price', 'term_price', 'annual_price', 'is_featured')
    list_filter = ('level', 'is_featured')
    search_fields = ('name', 'features')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'course_name', 'completion_date', 'verification_code')
    list_filter = ('completion_date',)
    search_fields = ('student_name', 'course_name', 'verification_code')


class ForumReplyInline(admin.TabularInline):
    model = ForumReply
    extra = 0


@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'body', 'author_name')
    inlines = [ForumReplyInline]


@admin.register(CommunityChallenge)
class CommunityChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'challenge_type', 'deadline', 'prize', 'is_active')
    list_filter = ('challenge_type', 'is_active', 'deadline')
    search_fields = ('title', 'description')


@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'location', 'deadline', 'is_active')
    list_filter = ('job_type', 'is_active', 'deadline')
    search_fields = ('title', 'company', 'description')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'is_featured', 'created_at')
    list_filter = ('resource_type', 'is_featured', 'created_at')
    search_fields = ('title', 'summary')


@admin.register(MentorAIInteraction)
class MentorAIInteractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'question')
    search_fields = ('name', 'question', 'answer')
    readonly_fields = ('created_at',)


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'score', 'created_at')
    list_filter = ('game', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at',)
