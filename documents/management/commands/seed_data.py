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
    help = "[h] Populates the database with synthetic articles using memory-safe batching."

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=1000000, help="Number of articles to create")
        parser.add_argument('--chunk-size', type=int, default=50000, help="Batch size per insertion loop")

    def handle(self, *args, **options):
        total_count = options['count']
        chunk_size = options['chunk_size']

        self.stdout.write(f"[o] Starting seeding of {total_count:,} records in batches of {chunk_size:,}...")

        created_so_far = 0

        while created_so_far < total_count:
            current_batch_size = min(chunk_size, total_count - created_so_far)

            # 1. Generate chunk in memory
            articles = [
                Article(
                    title=f"Article #{created_so_far + i}: " + " ".join(random.choices(WORDS, k=3)).title(),
                    content=" ".join(random.choices(WORDS, k=120))
                )
                for i in range(current_batch_size)
            ]

            # 2. Bulk insert chunk into PostgreSQL
            created_objects = Article.objects.bulk_create(articles, batch_size=5000)

            # 3. Compute SearchVector for newly created batch
            batch_ids = [obj.pk for obj in created_objects]
            Article.objects.filter(pk__in=batch_ids).update(
                search_vector=SearchVector('title', weight='A') + SearchVector('content', weight='B')
            )

            created_so_far += current_batch_size
            self.stdout.write(f"Progress: {created_so_far:,} / {total_count:,} records inserted.")

        self.stdout.write(self.style.SUCCESS(f"\n[o] Success. Seeded {total_count:,} records."))