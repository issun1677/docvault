from django.shortcuts import render, redirect  
from repository.forms import DocumentForm
from repository.models import Document
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


