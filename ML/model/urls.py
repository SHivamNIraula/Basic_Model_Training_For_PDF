from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('upload/', views.upload_document, name='upload_document'),
    path('query/<int:document_id>/', views.query_document, name='query_document'),
    path('history/', views.query_history, name='query_history'),
    path('api/query/', views.api_query, name='api_query'),
]