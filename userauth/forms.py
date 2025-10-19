from django import forms
from django.contrib.auth.models import User
from .models import Profile




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # use the actual model fields
        fields = ['biography', 'profile_picture', 'job_title', 'phone']
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
        }
