import random
from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from documents.models import Article

WORDS = [
    "database", "postgresql", "django", "search", "vector", "index", "performance",
    "optimization", "infrastructure", "backend", "cloud", "devops", "query", "latency",
    "python", "rust", "linux", "docker", "pipeline", "benchmark", "architecture", "scale"
]

class Command(BaseCommand):
    help = "[h] Populates the database with synthetic articles for testing"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=20000, help="Number of articles to create")

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(f"Generating {count} synthetic articles...")

        articles = [
            Article(
                title=f"Article #{i}: " + " ".join(random.choices(WORDS, k=3)).title(),
                content=" ".join(random.choices(WORDS, k=120))
            )
            for i in range(count)
        ]

        Article.objects.bulk_create(articles, batch_size=5000)

        self.stdout.write("Calculating search vectors and GIN indexes...")
        Article.objects.update(
            search_vector=SearchVector('title', weight='A') + SearchVector('content', weight='B')
        )
        self.stdout.write(self.style.SUCCESS(f"[o] Success. Created {count} articles."))