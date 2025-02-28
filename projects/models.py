from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('full name'), max_length=150, blank=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(_('active'), default=False)

    def __str__(self):
        return self.username

class Company(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class JobListing(models.Model):
    EXPERIENCE_CHOICES = [
        ('entry', _('Entry Level')),
        ('junior', _('Junior')),
        ('mid', _('Mid-Level')),
        ('senior', _('Senior')),
        ('lead', _('Lead')),
    ]

    JOB_TYPE_CHOICES = [
        ('full_time', _('Full Time')),
        ('part_time', _('Part Time')),
        ('contract', _('Contract')),
        ('freelance', _('Freelance')),
    ]

    LOCATION_TYPE_CHOICES = [
        ('remote', _('Remote')),
        ('onsite', _('On-site')),
        ('hybrid', _('Hybrid')),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    location = models.CharField(max_length=100, blank=True)
    salary = models.CharField(max_length=50)
    tags = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"

@receiver(post_save, sender=CustomUser)
def create_verification_token(sender, instance, created, **kwargs):
    if created:
        instance.verification_token = get_random_string(64)
        instance.save()

