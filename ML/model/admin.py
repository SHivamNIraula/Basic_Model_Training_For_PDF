from django.contrib import admin
from .models import Document, DocumentChunk, Query, RAGIndex


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_by', 'upload_date', 'is_processed', 'num_chunks']
    list_filter = ['is_processed', 'upload_date']
    search_fields = ['title', 'uploaded_by__username']
    readonly_fields = ['upload_date']


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ['document', 'chunk_index', 'created_at']
    list_filter = ['created_at']
    search_fields = ['document__title', 'content']


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ['user', 'document', 'created_at', 'response_time']
    list_filter = ['created_at']
    search_fields = ['user__username', 'question', 'document__title']
    readonly_fields = ['created_at']


@admin.register(RAGIndex)
class RAGIndexAdmin(admin.ModelAdmin):
    list_display = ['document', 'embedding_model', 'created_at', 'updated_at']
    list_filter = ['embedding_model', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
