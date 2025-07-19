from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    title = models.CharField(max_length=200)
    file_path = models.CharField(max_length=500)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    num_chunks = models.IntegerField(default=0)
    file_size = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.IntegerField()
    content = models.TextField()
    embedding_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['document', 'chunk_index']
    
    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"


class Query(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    response_time = models.FloatField(default=0.0)
    
    def __str__(self):
        return f"Query by {self.user.username} on {self.created_at}"


class RAGIndex(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name='rag_index')
    index_path = models.CharField(max_length=500)
    embedding_model = models.CharField(max_length=100, default='all-MiniLM-L6-v2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"RAG Index for {self.document.title}"
