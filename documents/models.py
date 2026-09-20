from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [
            # GIN Index to accelerate searches in milliseconds
            GinIndex(fields=['search_vector'], name='article_search_vector_gin'),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the search vector assigning more weight to the title than the content
        if 'update_fields' not in kwargs or 'search_vector' in kwargs.get('update_fields', []):
            Article.objects.filter(pk=self.pk).update(
                search_vector=SearchVector('title', weight='A') + SearchVector('content', weight='B')
            )

    def __str__(self):
        return self.title