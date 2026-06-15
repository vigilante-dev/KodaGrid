"""
Run all curriculum batches in sequence.
Usage: python manage.py setup_full_curriculum
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Run all curriculum generation batches (1-5)"

    def handle(self, *args, **options):
        batches = [
            ("generate_full_curriculum",  "Batch 1 — HTML5, CSS3, TypeScript, Java"),
            ("generate_curriculum_2",     "Batch 2 — Python, Django, Flask"),
            ("generate_curriculum_3",     "Batch 3 — React, Node.js, Bootstrap, TailwindCSS"),
            ("generate_curriculum_4",     "Batch 4 — SQL, MongoDB, C, Cybersecurity"),
            ("generate_curriculum_5",     "Batch 5 — Machine Learning, Deep Learning, Generative AI"),
        ]
        for cmd, label in batches:
            self.stdout.write(f"\n{label}")
            self.stdout.write("-" * 50)
            call_command(cmd)

        from academy.models import LearningPath, Lesson
        self.stdout.write(self.style.SUCCESS(
            f"\nComplete -- {LearningPath.objects.count()} paths, "
            f"{Lesson.objects.count()} lessons total."
        ))
