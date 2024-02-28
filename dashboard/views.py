# In your Django views.py

import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .forms import PostForm
from .models import Post
from django.urls import reverse


def analytics(request):
    return render(request,'analytics.html')


def logout_view(request):
    logout(request)
    # Redirect to the login page after logout
    return redirect(reverse('login'))


def fetch_analytics(request):
    api_url = 'https://65d87166c96fbb24c1bb8968.mockapi.io/posts'

    try:
        # Make a GET request to the mock API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for any HTTP error
        
        analytics_data = response.json()  # Extract JSON data from the response
        
        # Initialize counters for likes, shares, and comments
        likes = 0
        shares = 0
        comments = 0
        
        # Iterate over each post and sum up the likes, shares, and comments
        for post in analytics_data:
            likes += post.get('likes', 0)
            shares += post.get('shares', 0)
            comments += post.get('comments', 0)

        # Construct a dictionary with the fetched data
        data = {
            'likes': likes,
            'shares': shares,
            'comments': comments
        }

        return JsonResponse(data)
    
    except requests.RequestException as e:
        # Handle any HTTP request errors
        return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        # Handle any other unexpected errors
        return JsonResponse({'error': str(e)}, status=500)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Log the user in
            user = form.get_user()
            login(request, user)
            # Redirect to a protected page or dashboard after successful login
            return redirect('home')  # Change 'home' to your desired URL
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
    

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # After registering, redirect to the login page
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if 'schedule' in request.POST:
                post.status = Post.SCHEDULED
                post.publish_date = request.POST.get('publish_date')  # Get scheduled publish date
            else:
                post.status = Post.PUBLISHED
            post.save()
            return redirect('home')  # Redirect to home page after post creation
    else:
        form = PostForm()
    return render(request, 'create-post.html', {'form': form})

def display_post(request):
    # Retrieve all posts from the database
    posts = Post.objects.all()
    # Pass the queryset of posts to the template
    return render(request, 'display-post.html', {'posts': posts})