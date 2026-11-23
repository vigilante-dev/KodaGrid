from django.contrib import admin, messages
from django.db import transaction
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'username',
        'email',
        'phone_number',
        'career_interest',
        'approval_status',
        'date_joined',
    )
    list_filter = ('approval_status', 'date_joined')
    search_fields = ('name', 'email', 'phone_number', 'user__username')
    exclude = ('profile_picture',)
    fields = (
        'name',
        'username',
        'email',
        'phone_number',
        'career_interest',
        'approval_status',
        'student_photo',
        'date_joined',
        'approved_at',
        'reviewed_at',
        'reviewed_by',
        'bio',
    )
    readonly_fields = (
        'username',
        'approval_status',
        'student_photo',
        'date_joined',
        'approved_at',
        'reviewed_at',
        'reviewed_by',
    )
    actions = ('approve_applications', 'reject_applications')
    list_select_related = ('user', 'reviewed_by')

    @admin.display(description='Username', ordering='user__username')
    def username(self, student):
        return student.user.get_username() if student.user_id else '—'

    @admin.display(description='Student photo')
    def student_photo(self, student):
        if not student or not student.pk or not student.profile_picture:
            return 'No photo uploaded'
        photo_url = reverse('student_photo', args=(student.pk,))
        return format_html(
            '<img src="{}" alt="Student photo" style="max-height: 180px; max-width: 180px; object-fit: cover;">',
            photo_url,
        )

    @admin.action(description='Approve selected student applications')
    def approve_applications(self, request, queryset):
        self._review_applications(request, queryset, Student.ApprovalStatus.APPROVED)

    @admin.action(description='Reject selected student applications')
    def reject_applications(self, request, queryset):
        self._review_applications(request, queryset, Student.ApprovalStatus.REJECTED)

    @transaction.atomic
    def _review_applications(self, request, queryset, status):
        now = timezone.now()
        reviewed = 0
        skipped = 0
        for student in queryset.select_related('user'):
            user = student.user
            if user is None or user.is_staff or user.is_superuser:
                skipped += 1
                continue

            student.approval_status = status
            student.reviewed_at = now
            student.reviewed_by = request.user
            student.approved_at = now if status == Student.ApprovalStatus.APPROVED else None
            student.save(update_fields=(
                'approval_status', 'reviewed_at', 'reviewed_by', 'approved_at',
            ))

            user.is_active = status == Student.ApprovalStatus.APPROVED
            user.save(update_fields=('is_active',))
            reviewed += 1

        label = 'approved' if status == Student.ApprovalStatus.APPROVED else 'rejected'
        self.message_user(request, f'{reviewed} application(s) {label}.', messages.SUCCESS)
        if skipped:
            self.message_user(
                request,
                f'{skipped} record(s) were skipped because they have no student account or belong to staff.',
                messages.WARNING,
            )
