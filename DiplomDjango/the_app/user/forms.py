from django import forms
from .models import User
from .models import Idea


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'age']
        widgets = {
            'password': forms.PasswordInput(),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age']
        help_texts = {
            'username': None,
        }


class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['topic', 'description']
        widgets = {
            'topic': forms.TextInput(attrs={'placeholder': 'Тема'}),
            'description': forms.Textarea(attrs={'placeholder': 'Идея'}),
        }