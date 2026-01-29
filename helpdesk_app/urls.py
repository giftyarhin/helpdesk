from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public pages
    path('', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    
    # Admin pages
    path('inbox/', views.inbox_view, name='inbox'),
    path('message/<int:message_id>/', views.message_detail_view, name='message_detail'),
    path('message/<int:message_id>/mark-read/', views.mark_as_read, name='mark_as_read'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
