from django import forms
from .models import Curso, Tutor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TutorForm(forms.ModelForm):
    
    class Meta:
        model = Tutor
        fields = "__all__"
        
class CursoForm(forms.ModelForm):
    
    class Meta:
        model = Curso
        fields = "__all__"
        
class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
        