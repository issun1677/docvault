from django.shortcuts import render, redirect  
from repository.forms import DocumentForm
from repository.models import Document
from django.utils import timezone
from datetime import timedelta
# Create your views here.

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            uploaded_file = request.FILES['file']
            document.original_file_name = uploaded_file.name
            document.file_size = uploaded_file.size
            document.mime_type = uploaded_file.content_type
            document.save()
            return redirect('list_document')
    else:
        form = DocumentForm()      


    context = {'form': DocumentForm}
    return render(request, 'repository/upload.html', context)



def list_document(request):
    document_view = Document.objects.all()
    context = {"documents": document_view}
    return render(request, 'repository/document_list.html', context)


def dashboard(request):
    documents = Document.objects.all()
    total_documents = documents.count()
    
    # Calculate total storage used
    total_size = sum(doc.file_size for doc in documents)
    total_size_mb = round(total_size / (1024 * 1024), 2) if total_size > 0 else 0
    
    # Get documents from the last 7 days
    week_ago = timezone.now() - timedelta(days=7)
    recent_count = documents.filter(uploaded_at__gte=week_ago).count()
    
    # Get 5 most recent documents
    recent_documents = documents.order_by('-uploaded_at')[:5]
    
    context = {
        'total_documents': total_documents,
        'total_size_mb': total_size_mb,
        'recent_count': recent_count,
        'recent_documents': recent_documents,
    }
    return render(request, 'repository/dashboard.html', context)