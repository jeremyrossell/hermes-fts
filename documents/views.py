import time
from django.http import JsonResponse
from django.contrib.postgres.search import SearchQuery
from .models import Article

def search_api(request):
    query_str = request.GET.get('q', '')
    mode = request.GET.get('mode', 'fast')

    if not query_str:
        return JsonResponse({'error': 'Parameter ?q= is required'}, status=400)

    t0 = time.perf_counter()

    if mode == 'slow':
        qs = Article.objects.filter(content__icontains=query_str)
    else:
        qs = Article.objects.filter(search_vector=SearchQuery(query_str))

    results = list(qs.values('id', 'title')[:20])
    execution_time_ms = (time.perf_counter() - t0) * 1000

    return JsonResponse({
        'mode': mode,
        'query': query_str,
        'execution_time_ms': round(execution_time_ms, 2),
        'count': len(results),
        'results': results
    })