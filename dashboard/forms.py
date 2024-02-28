from django import forms
from .models import Post
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login



class CustomUserCreationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    reEnterpassword = forms.CharField(widget=forms.PasswordInput)
   

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        reEnterpassword = cleaned_data.get('reEnterpassword')
        if password and reEnterpassword and password != reEnterpassword:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username=username, password=password)
        return user
    
from django.contrib.auth import authenticate

class CustomUserLoginForm(AuthenticationForm):
    def login_user(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'video', 'photo']   
        
        