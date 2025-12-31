from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.utils import timezone
from .models import About, Skill, Project, Experience, BlogPost, ContactMessage, SocialMediaLink
from .forms import ContactForm, AboutForm, SkillForm, ProjectForm, ExperienceForm, BlogPostForm, SocialMediaLinkForm

# Frontend Views

def home(request):
    about = About.objects.first()
    skills = Skill.objects.all()[:6]  # Show top 6 skills
    projects = Project.objects.all()[:3]  # Show latest 3 projects
    experiences = Experience.objects.filter(is_education=False).order_by('-start_date')[:3]
    social_links = SocialMediaLink.objects.all()
    return render(request, 'portfolio/home.html', {
        'about': about,
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
        'social_links': social_links,
    })

def about_view(request):
    about = About.objects.first()
    return render(request, 'portfolio/about.html', {'about': about})

def skills_view(request):
    skills = Skill.objects.all()
    return render(request, 'portfolio/skills.html', {'skills': skills})

def projects_view(request):
    projects = Project.objects.all()
    return render(request, 'portfolio/projects.html', {'projects': projects})

def experience_view(request):
    work_experience = Experience.objects.filter(is_education=False).order_by('-start_date')
    education = Experience.objects.filter(is_education=True).order_by('-start_date')
    return render(request, 'portfolio/experience.html', {
        'work_experience': work_experience,
        'education': education,
    })

def blog_view(request):
    published_posts = BlogPost.objects.filter(published=True).order_by('-published_at')
    paginator = Paginator(published_posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'portfolio/blog.html', {'page_obj': page_obj})

def blog_detail_view(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, 'portfolio/blog_detail.html', {'post': post})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'portfolio/contact.html', {'form': form})

# Admin Views (Simplified - No Authentication Required)

def admin_login(request):
    # Redirect directly to dashboard - no login required
    return redirect('admin_dashboard')

def admin_logout(request):
    # Simple logout - just redirect to login
    return redirect('admin_login')

def admin_dashboard(request):
    stats = {
        'total_projects': Project.objects.count(),
        'total_skills': Skill.objects.count(),
        'total_experiences': Experience.objects.count(),
        'total_blog_posts': BlogPost.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'total_social_links': SocialMediaLink.objects.count(),
    }
    return render(request, 'portfolio/admin/dashboard.html', {'stats': stats})

# CRUD for About
def admin_about_list(request):
    about = About.objects.first()
    return render(request, 'portfolio/admin/about_list.html', {'about': about})

def admin_about_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        profile_image = request.FILES.get('profile_image')
        About.objects.create(title=title, description=description, profile_image=profile_image)
        messages.success(request, 'About section created successfully!')
        return redirect('admin_about_list')
    return render(request, 'portfolio/admin/about_form.html')

def admin_about_update(request, pk):
    about = get_object_or_404(About, pk=pk)
    if request.method == 'POST':
        about.title = request.POST.get('title')
        about.description = request.POST.get('description')
        if request.FILES.get('profile_image'):
            about.profile_image = request.FILES.get('profile_image')
        about.save()
        messages.success(request, 'About section updated successfully!')
        return redirect('admin_about_list')
    return render(request, 'portfolio/admin/about_form.html', {'about': about})

def admin_about_delete(request, pk):
    about = get_object_or_404(About, pk=pk)
    about.delete()
    messages.success(request, 'About section deleted successfully!')
    return redirect('admin_about_list')

# CRUD for Skills
def admin_skills_list(request):
    skills = Skill.objects.all()
    return render(request, 'portfolio/admin/skills_list.html', {'skills': skills})

def admin_skills_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        level = request.POST.get('level')
        category = request.POST.get('category')
        Skill.objects.create(name=name, level=level, category=category)
        messages.success(request, 'Skill created successfully!')
        return redirect('admin_skills_list')
    return render(request, 'portfolio/admin/skills_form.html')

def admin_skills_update(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        skill.name = request.POST.get('name')
        skill.level = request.POST.get('level')
        skill.category = request.POST.get('category')
        skill.save()
        messages.success(request, 'Skill updated successfully!')
        return redirect('admin_skills_list')
    return render(request, 'portfolio/admin/skills_form.html', {'skill': skill})

def admin_skills_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    skill.delete()
    messages.success(request, 'Skill deleted successfully!')
    return redirect('admin_skills_list')

# CRUD for Projects
def admin_projects_list(request):
    projects = Project.objects.all()
    return render(request, 'portfolio/admin/projects_list.html', {'projects': projects})

def admin_projects_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        url = request.POST.get('url')
        github_url = request.POST.get('github_url')
        technologies = request.POST.get('technologies')
        Project.objects.create(
            title=title, description=description, image=image,
            url=url, github_url=github_url, technologies=technologies
        )
        messages.success(request, 'Project created successfully!')
        return redirect('admin_projects_list')
    return render(request, 'portfolio/admin/projects_form.html')

def admin_projects_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.description = request.POST.get('description')
        if request.FILES.get('image'):
            project.image = request.FILES.get('image')
        project.url = request.POST.get('url')
        project.github_url = request.POST.get('github_url')
        project.technologies = request.POST.get('technologies')
        project.save()
        messages.success(request, 'Project updated successfully!')
        return redirect('admin_projects_list')
    return render(request, 'portfolio/admin/projects_form.html', {'project': project})

def admin_projects_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    messages.success(request, 'Project deleted successfully!')
    return redirect('admin_projects_list')

# CRUD for Experience
def admin_experience_list(request):
    experiences = Experience.objects.all()
    return render(request, 'portfolio/admin/experience_list.html', {'experiences': experiences})

def admin_experience_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_current = request.POST.get('is_current') == 'on'
        is_education = request.POST.get('is_education') == 'on'
        Experience.objects.create(
            title=title, company=company, description=description,
            start_date=start_date, end_date=end_date, is_current=is_current, is_education=is_education
        )
        messages.success(request, 'Experience created successfully!')
        return redirect('admin_experience_list')
    return render(request, 'portfolio/admin/experience_form.html')

def admin_experience_update(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        experience.title = request.POST.get('title')
        experience.company = request.POST.get('company')
        experience.description = request.POST.get('description')
        experience.start_date = request.POST.get('start_date')
        experience.end_date = request.POST.get('end_date')
        experience.is_current = request.POST.get('is_current') == 'on'
        experience.is_education = request.POST.get('is_education') == 'on'
        experience.save()
        messages.success(request, 'Experience updated successfully!')
        return redirect('admin_experience_list')
    return render(request, 'portfolio/admin/experience_form.html', {'experience': experience})

def admin_experience_delete(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    experience.delete()
    messages.success(request, 'Experience deleted successfully!')
    return redirect('admin_experience_list')

# CRUD for Blog Posts
def admin_blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'portfolio/admin/blog_list.html', {'posts': posts})

def admin_blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt')
        image = request.FILES.get('image')
        published = request.POST.get('published') == 'on'
        slug = slugify(title)
        published_at = timezone.now() if published else None
        BlogPost.objects.create(
            title=title, slug=slug, content=content, excerpt=excerpt,
            image=image, published=published, published_at=published_at
        )
        messages.success(request, 'Blog post created successfully!')
        return redirect('admin_blog_list')
    return render(request, 'portfolio/admin/blog_form.html')

def admin_blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.excerpt = request.POST.get('excerpt')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.published = request.POST.get('published') == 'on'
        post.slug = slugify(post.title)
        if post.published and not post.published_at:
            post.published_at = timezone.now()
        post.save()
        messages.success(request, 'Blog post updated successfully!')
        return redirect('admin_blog_list')
    return render(request, 'portfolio/admin/blog_form.html', {'post': post})

def admin_blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    messages.success(request, 'Blog post deleted successfully!')
    return redirect('admin_blog_list')

# CRUD for Contact Messages
def admin_messages_list(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'portfolio/admin/messages_list.html', {'messages': messages_list})

def admin_messages_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'portfolio/admin/messages_detail.html', {'message': message})

def admin_messages_delete(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    message.delete()
    messages.success(request, 'Message deleted successfully!')
    return redirect('admin_messages_list')

# CRUD for Social Media Links
def admin_social_media_list(request):
    social_links = SocialMediaLink.objects.all()
    return render(request, 'portfolio/admin/social_media_list.html', {'social_links': social_links})

def admin_social_media_create(request):
    if request.method == 'POST':
        form = SocialMediaLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Social media link created successfully!')
            return redirect('admin_social_media_list')
    else:
        form = SocialMediaLinkForm()
    return render(request, 'portfolio/admin/social_media_form.html', {'form': form})

def admin_social_media_update(request, pk):
    social_link = get_object_or_404(SocialMediaLink, pk=pk)
    if request.method == 'POST':
        form = SocialMediaLinkForm(request.POST, instance=social_link)
        if form.is_valid():
            form.save()
            messages.success(request, 'Social media link updated successfully!')
            return redirect('admin_social_media_list')
    else:
        form = SocialMediaLinkForm(instance=social_link)
    return render(request, 'portfolio/admin/social_media_form.html', {'form': form, 'social_link': social_link})

def admin_social_media_delete(request, pk):
    social_link = get_object_or_404(SocialMediaLink, pk=pk)
    social_link.delete()
    messages.success(request, 'Social media link deleted successfully!')
    return redirect('admin_social_media_list')
