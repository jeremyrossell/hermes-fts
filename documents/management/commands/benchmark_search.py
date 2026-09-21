import time
from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchQuery
from documents.models import Article

class Command(BaseCommand):
    help = "[h] Compares speed between icontains (Sequential Scan) and GIN Index (Full-Text Search)"

    def add_arguments(self, parser):
        parser.add_argument('--query', type=str, default='infrastructure')

    def handle(self, *args, **options):
        query_str = options['query']
        total_records = Article.objects.count()

        self.stdout.write(f"\n=== SEARCH BENCHMARK ({total_records:,} records) ===")
        self.stdout.write(f"Query term: '{query_str}'\n")

        # 1. Traditional search (full table scan)
        t0 = time.perf_counter()
        slow_results = list(Article.objects.filter(content__icontains=query_str)[:50])
        slow_time = (time.perf_counter() - t0) * 1000

        # 2. PostgreSQL Full-Text Search (GIN Index)
        t0 = time.perf_counter()
        fast_results = list(Article.objects.filter(search_vector=SearchQuery(query_str))[:50])
        fast_time = (time.perf_counter() - t0) * 1000

        self.stdout.write(f"Sequential Scan:    {slow_time:.2f} ms")
        self.stdout.write(f"GIN Index:          {fast_time:.2f} ms")

        if fast_time > 0:
            speedup = slow_time / fast_time
            self.stdout.write(self.style.SUCCESS(f"\n[o] Search with GIN index is {speedup:.1f}x faster."))