from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from django.utils.translation import gettext as _
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from django.utils.crypto import get_random_string
from .models import JobListing, Company, Application, CustomUser
from .forms import JobListingForm, ApplicationForm, CompanyForm, CustomUserCreationForm
from django.urls import reverse
from .forms import CustomUserCreationForm
import logging

logger = logging.getLogger(__name__)


def home(request):
    recent_jobs = JobListing.objects.filter(is_active=True).order_by('-created_at')[:6]
    return render(request, 'home.html', {'recent_jobs': recent_jobs})

def search_jobs(request):
    query = request.GET.get('q')
    if query:
        results = JobListing.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        ).filter(is_active=True)
    else:
        results = JobListing.objects.filter(is_active=True)
    return render(request, 'search_results.html', {'results': results, 'query': query})

@login_required
def dashboard(request):
    if hasattr(request.user, 'company'):
        job_listings = JobListing.objects.filter(company=request.user.company)
        return render(request, 'dashboard.html', {'job_listings': job_listings, 'is_company': True})
    else:
        applications = Application.objects.filter(applicant=request.user)
        return render(request, 'dashboard.html', {'applications': applications, 'is_company': False})

@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            if hasattr(request.user, 'company'):
                job.company = request.user.company
            else:
                company, created = Company.objects.get_or_create(user=request.user, defaults={'name': f"{request.user.username}'s Company"})
                job.company = company
            job.save()
            messages.success(request, _('Job listing created successfully.'))
            return redirect('dashboard')
    else:
        form = JobListingForm()
    
    return render(request, 'job_form.html', {'form': form, 'is_create': True})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id, company=request.user.company)
    
    if request.method == 'POST':
        form = JobListingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, _('Job listing updated successfully.'))
            return redirect('dashboard')
    else:
        form = JobListingForm(instance=job)
    
    return render(request, 'job_form.html', {'form': form, 'is_create': False})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id, company=request.user.company)
    job.delete()
    messages.success(request, _('Job listing deleted successfully.'))
    return redirect('dashboard')

def job_detail(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    job.views += 1
    job.save()
    return render(request, 'job_detail.html', {'job': job})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, _('Ariza muvaffaqiyatli yuborildi.'))
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.verification_token = get_random_string(64)
            user.save()
            
            subject = "Elektron pochtangizni tasdiqlang"
            verification_url = request.build_absolute_uri(
                reverse('verify_email', kwargs={'token': user.verification_token})
            )
            html_message = render_to_string('email/verification_email.html', {
                'user': user,
                'verification_url': verification_url
            })
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False
                )
                messages.success(
                    request,
                    "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi. Iltimos, elektron pochtangizni tasdiqlang."
                )
                return redirect('login')
            except Exception as e:
                logger.error(f"Error sending email: {str(e)}")
                messages.error(
                    request,
                    "Elektron pochta yuborishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
                )
                user.delete() 
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})



@login_required
def create_company(request):
    if hasattr(request.user, 'company'):
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            messages.success(request, _('Company profile created successfully.'))
            return redirect('dashboard')
    else:
        form = CompanyForm()
    return render(request, 'create_company.html', {'form': form})


def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token, is_active=False)
        user.is_active = True
        user.is_verified = True
        user.verification_token = ''
        user.save()
        messages.success(request, "Elektron pochtangiz tasdiqlandi. Endi tizimga kirishingiz mumkin.")
    except CustomUser.DoesNotExist:
        messages.error(request, "Noto'g'ri tasdiqlash havolasi.")
    
    return redirect('login')



def send_verification_email(user):
    subject = _('Verify your email address')
    verification_url = reverse('verify_email', kwargs={'token': user.verification_token})
    full_verification_url = f"{settings.BASE_URL}{verification_url}"
    html_message = render_to_string('email/verification_email.html', {
        'user': user,
        'verification_url': full_verification_url
    })
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

