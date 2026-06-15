from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image

from gallery.models import GalleryImage


class Command(BaseCommand):
    help = 'Analyze, optimize, caption, and place academy images from the images folder.'

    def add_arguments(self, parser):
        parser.add_argument('--source', default='images', help='Folder containing source images.')
        parser.add_argument('--max-width', type=int, default=1400)

    def handle(self, *args, **options):
        source = Path(options['source'])
        if not source.exists():
            self.stderr.write(self.style.ERROR(f'Image folder not found: {source}'))
            return

        count = 0
        for path in source.iterdir():
            if path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp'}:
                continue
            analysis = self.analyze(path)
            image_bytes = self.optimize(path, options['max_width'])
            title = analysis['title']
            gallery_item, _created = GalleryImage.objects.update_or_create(
                title=title,
                defaults={
                    'category': analysis['category'],
                    'caption': analysis['caption'],
                    'detected_subject': analysis['subject'],
                    'detected_activity': analysis['activity'],
                    'age_group': analysis['age_group'],
                    'educational_relevance': analysis['relevance'],
                    'suggested_placement': analysis['placement'],
                    'optimized_from': str(path),
                },
            )
            filename = f'{slugify(title)}.jpg'
            gallery_item.image.save(filename, ContentFile(image_bytes.getvalue()), save=True)
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Analyzed and optimized {count} image(s).'))

    def analyze(self, path):
        name = path.stem.replace('_', ' ').replace('-', ' ')
        lower = name.lower()

        if any(word in lower for word in ['developer', 'coding', 'computer', 'programming', 'language']):
            return {
                'title': self.clean_title(name),
                'category': 'training',
                'subject': 'young technology learners and developer-focused visuals',
                'activity': 'coding practice, programming study, or software project work',
                'age_group': 'teenagers and young adults',
                'relevance': 'Strong fit for learning paths, programming courses, and hero storytelling.',
                'placement': 'Hero Section or Featured Courses',
                'caption': 'Learners building confidence through practical coding and software projects.',
            }
        if any(word in lower for word in ['data', 'analytics']):
            return {
                'title': self.clean_title(name),
                'category': 'projects',
                'subject': 'data and analytics learning visuals',
                'activity': 'data exploration, dashboards, and analytical thinking',
                'age_group': 'college students and young professionals',
                'relevance': 'Best used for data science, AI, and career-readiness sections.',
                'placement': 'Learning Platform or Resource Center',
                'caption': 'Students turn data into insight through analytics and project-based learning.',
            }
        if any(word in lower for word in ['believed', 'girl', 'woman', 'herself']):
            return {
                'title': self.clean_title(name),
                'category': 'outreach',
                'subject': 'aspiring girls and young women in technology',
                'activity': 'confidence building, mentorship, and coding inspiration',
                'age_group': 'high school and college learners',
                'relevance': 'Best suited for Girls Program, mentorship, scholarships, and success stories.',
                'placement': 'Girls Program or Testimonials',
                'caption': 'Girls in technology gain confidence, mentorship, and a pathway into digital careers.',
            }
        return {
            'title': self.clean_title(name),
            'category': 'training',
            'subject': 'student learning and technology inspiration',
            'activity': 'digital skills learning and academy engagement',
            'age_group': 'teenagers and young adults',
            'relevance': 'Useful for academy gallery, community, and student success storytelling.',
            'placement': 'Gallery or Community Section',
            'caption': 'A CodeSavannah Academy moment focused on learning, growth, and opportunity.',
        }

    def optimize(self, path, max_width):
        with Image.open(path) as image:
            image = image.convert('RGB')
            if image.width > max_width:
                ratio = max_width / image.width
                image = image.resize((max_width, int(image.height * ratio)))
            output = BytesIO()
            image.save(output, format='JPEG', quality=84, optimize=True, progressive=True)
            output.seek(0)
            return output

    def clean_title(self, value):
        title = ' '.join(value.split())
        if len(title) > 70:
            title = f'{title[:67]}...'
        return title.title()
