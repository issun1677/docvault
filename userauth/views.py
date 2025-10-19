from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Profile
from repository.models import Document
from datetime import timedelta
from django.utils import timezone
from .forms import ProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('dashboard')
    
    else:
        form = UserCreationForm()

    return render (request, "userauth/user_register.html", {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'userauth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def show_profile(request):
    profile = request.user.profile
    documents = Document.objects.filter(uploaded_by=request.user)

    #Calculating User's Document statistics
    total_documents = documents.count()
    total_storage = sum(doc.file_size for doc in documents)
    total_storage_mb = round(total_storage / (1024 * 1024), 2) if total_storage > 0 else 0

    # recent uploads "weekly"
    week_ago = timezone.now() - timedelta(days=7)
    recent_uploads = documents.filter(uploaded_at__gte=week_ago).count()

    context = {
        'profile': profile,
        'total_documents': total_documents,
        'total_storage_mb': total_storage_mb,
        'recent_uploads': recent_uploads,
    }

    return render(request, 'userauth/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':        
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=profile)

    context = {
        'profile_form': profile_form,
    }

    return render(request, 'userauth/edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'userauth/change_password.html', {'form': form})

