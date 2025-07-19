import os
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Document, DocumentChunk, Query, RAGIndex
from .rag_processor import RAGProcessor
import json


@login_required
def upload_document(request):
    if request.method == 'POST':
        if 'pdf_file' not in request.FILES:
            messages.error(request, 'No file uploaded')
            return redirect('upload_document')
        
        pdf_file = request.FILES['pdf_file']
        title = request.POST.get('title', pdf_file.name)
        
        # Save file
        file_path = default_storage.save(f'documents/{pdf_file.name}', ContentFile(pdf_file.read()))
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        
        # Create document record
        document = Document.objects.create(
            title=title,
            file_path=full_path,
            uploaded_by=request.user,
            file_size=pdf_file.size
        )
        
        # Process the document in background (for now, process immediately)
        try:
            process_document_rag(document.id)
            messages.success(request, 'Document uploaded and processed successfully!')
        except Exception as e:
            messages.error(request, f'Error processing document: {str(e)}')
        
        return redirect('document_list')
    
    return render(request, 'model/upload_document.html')


def process_document_rag(document_id):
    """Process document to create RAG index."""
    document = Document.objects.get(id=document_id)
    
    # Initialize RAG processor
    rag_processor = RAGProcessor()
    
    # Process PDF
    result = rag_processor.process_pdf(document.file_path)
    
    if 'error' in result:
        raise Exception(result['error'])
    
    # Save chunks to database
    for i, doc_chunk in enumerate(rag_processor.documents):
        DocumentChunk.objects.create(
            document=document,
            chunk_index=i,
            content=doc_chunk.page_content
        )
    
    # Save RAG index
    index_path = os.path.join(settings.MEDIA_ROOT, f'indexes/document_{document_id}.pkl')
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    rag_processor.save_index(index_path)
    
    # Create RAG index record
    RAGIndex.objects.create(
        document=document,
        index_path=index_path
    )
    
    # Update document
    document.is_processed = True
    document.num_chunks = result['num_chunks']
    document.save()


@login_required
def document_list(request):
    documents = Document.objects.filter(uploaded_by=request.user).order_by('-upload_date')
    return render(request, 'model/document_list.html', {'documents': documents})


@login_required
def query_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, uploaded_by=request.user)
    
    if not document.is_processed:
        messages.error(request, 'Document is still being processed. Please wait.')
        return redirect('document_list')
    
    if request.method == 'POST':
        question = request.POST.get('question')
        
        if not question:
            messages.error(request, 'Please enter a question')
            return render(request, 'model/query_document.html', {'document': document})
        
        start_time = time.time()
        
        try:
            # Load RAG index
            rag_index = document.rag_index
            rag_processor = RAGProcessor()
            
            if not rag_processor.load_index(rag_index.index_path):
                messages.error(request, 'Error loading document index')
                return render(request, 'model/query_document.html', {'document': document})
            
            # Get answer with context
            result = rag_processor.get_answer_with_context(question, k=3)
            
            if 'error' in result:
                messages.error(request, result['error'])
                return render(request, 'model/query_document.html', {'document': document})
            
            # Create a simple answer from context (you can enhance this with actual LLM)
            answer = f"Based on the Constitution:\n\n{result['context']}"
            
            response_time = time.time() - start_time
            
            # Save query
            query = Query.objects.create(
                user=request.user,
                question=question,
                answer=answer,
                document=document,
                response_time=response_time
            )
            
            return render(request, 'model/query_document.html', {
                'document': document,
                'query': query,
                'similar_docs': result['similar_documents']
            })
            
        except Exception as e:
            messages.error(request, f'Error processing query: {str(e)}')
    
    return render(request, 'model/query_document.html', {'document': document})


@login_required
def query_history(request):
    queries = Query.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'model/query_history.html', {'queries': queries})


@csrf_exempt
def api_query(request):
    """API endpoint for querying documents."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        document_id = data.get('document_id')
        question = data.get('question')
        
        if not document_id or not question:
            return JsonResponse({'error': 'document_id and question are required'}, status=400)
        
        document = Document.objects.get(id=document_id)
        
        if not document.is_processed:
            return JsonResponse({'error': 'Document is still being processed'}, status=400)
        
        # Load RAG index
        rag_index = document.rag_index
        rag_processor = RAGProcessor()
        
        if not rag_processor.load_index(rag_index.index_path):
            return JsonResponse({'error': 'Error loading document index'}, status=500)
        
        # Get answer with context
        result = rag_processor.get_answer_with_context(question, k=3)
        
        if 'error' in result:
            return JsonResponse({'error': result['error']}, status=500)
        
        return JsonResponse({
            'question': question,
            'context': result['context'],
            'similar_documents': result['similar_documents'],
            'document_title': document.title
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
