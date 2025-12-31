from django.urls import path
from . import views

urlpatterns = [
    # Frontend URLs
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('skills/', views.skills_view, name='skills'),
    path('projects/', views.projects_view, name='projects'),
    path('experience/', views.experience_view, name='experience'),
    path('blog/', views.blog_view, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    path('contact/', views.contact_view, name='contact'),

    # Admin URLs
    path('manage/login/', views.admin_login, name='admin_login'),
    path('manage/logout/', views.admin_logout, name='admin_logout'),
    path('manage/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # About CRUD
    path('manage/about/', views.admin_about_list, name='admin_about_list'),
    path('manage/about/create/', views.admin_about_create, name='admin_about_create'),
    path('manage/about/<int:pk>/update/', views.admin_about_update, name='admin_about_update'),
    path('manage/about/<int:pk>/delete/', views.admin_about_delete, name='admin_about_delete'),

    # Skills CRUD
    path('manage/skills/', views.admin_skills_list, name='admin_skills_list'),
    path('manage/skills/create/', views.admin_skills_create, name='admin_skills_create'),
    path('manage/skills/<int:pk>/update/', views.admin_skills_update, name='admin_skills_update'),
    path('manage/skills/<int:pk>/delete/', views.admin_skills_delete, name='admin_skills_delete'),

    # Projects CRUD
    path('manage/projects/', views.admin_projects_list, name='admin_projects_list'),
    path('manage/projects/create/', views.admin_projects_create, name='admin_projects_create'),
    path('manage/projects/<int:pk>/update/', views.admin_projects_update, name='admin_projects_update'),
    path('manage/projects/<int:pk>/delete/', views.admin_projects_delete, name='admin_projects_delete'),

    # Experience CRUD
    path('manage/experience/', views.admin_experience_list, name='admin_experience_list'),
    path('manage/experience/create/', views.admin_experience_create, name='admin_experience_create'),
    path('manage/experience/<int:pk>/update/', views.admin_experience_update, name='admin_experience_update'),
    path('manage/experience/<int:pk>/delete/', views.admin_experience_delete, name='admin_experience_delete'),

    # Blog CRUD
    path('manage/blog/', views.admin_blog_list, name='admin_blog_list'),
    path('manage/blog/create/', views.admin_blog_create, name='admin_blog_create'),
    path('manage/blog/<int:pk>/update/', views.admin_blog_update, name='admin_blog_update'),
    path('manage/blog/<int:pk>/delete/', views.admin_blog_delete, name='admin_blog_delete'),

    # Messages CRUD
    path('manage/messages/', views.admin_messages_list, name='admin_messages_list'),
    path('manage/messages/<int:pk>/', views.admin_messages_detail, name='admin_messages_detail'),
    path('manage/messages/<int:pk>/delete/', views.admin_messages_delete, name='admin_messages_delete'),

    # Social Media CRUD
    path('manage/social-media/', views.admin_social_media_list, name='admin_social_media_list'),
    path('manage/social-media/create/', views.admin_social_media_create, name='admin_social_media_create'),
    path('manage/social-media/<int:pk>/update/', views.admin_social_media_update, name='admin_social_media_update'),
    path('manage/social-media/<int:pk>/delete/', views.admin_social_media_delete, name='admin_social_media_delete'),
]
