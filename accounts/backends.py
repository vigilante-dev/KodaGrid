from django.contrib.auth.backends import ModelBackend

from academy.models import TrainerProfile

from .models import Student


class StudentApprovalBackend(ModelBackend):
    """Require approval for student profiles while preserving staff access."""

    @staticmethod
    def user_is_approved(user):
        if not user or not user.is_active:
            return False
        if user.is_staff or user.is_superuser:
            return True
        try:
            profile = user.student_profile
        except Student.DoesNotExist:
            try:
                trainer_profile = user.trainer_profile
            except TrainerProfile.DoesNotExist:
                return False
            return trainer_profile.is_approved
        return profile.approval_status == Student.ApprovalStatus.APPROVED

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        return user if self.user_is_approved(user) else None

    def get_user(self, user_id):
        user = super().get_user(user_id)
        return user if self.user_is_approved(user) else None
