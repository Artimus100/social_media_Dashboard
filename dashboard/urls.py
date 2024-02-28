from django.urls import path
from . import views # Assuming you have a view for analytics

urlpatterns = [
    # Other URL patterns
    path('', views.analytics, name='home'),
     path('login/', views.login_view, name='login'),
    
    # URL pattern for the logout view
    path('logout/', views.logout_view, name='logout'),
    
    # URL pattern for the register view
    path('register/', views.register_view, name='register'),
    
    path('display-post/', views.display_post, name='display'),


]