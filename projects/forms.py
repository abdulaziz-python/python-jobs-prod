from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import JobListing, Application, Company, CustomUser
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=_("Elektron pochta"),
        error_messages={
            'unique': _("Bu elektron pochta allaqachon ro'yxatdan o'tgan."),
            'invalid': _("Noto'g'ri elektron pochta manzili."),
        }
    )
    name = forms.CharField(
        max_length=150,
        required=True,
        label=_("To'liq ism"),
        error_messages={
            'required': _("Iltimos, to'liq ismingizni kiriting."),
        }
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'password1', 'password2']
        labels = {
            'username': _("Foydalanuvchi nomi"),
        }
        error_messages = {
            'username': {
                'unique': _("Bu foydalanuvchi nomi allaqachon band."),
                'invalid': _("Foydalanuvchi nomi faqat harflar, raqamlar va @/./+/-/_ belgilarini o'z ichiga olishi mumkin."),
            }
        }

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError(_("Parol kamida 8 ta belgidan iborat bo'lishi kerak."))
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError(_("Parol kamida bitta katta harf o'z ichiga olishi kerak."))
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError(_("Parol kamida bitta kichik harf o'z ichiga olishi kerak."))
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError(_("Parol kamida bitta raqam o'z ichiga olishi kerak."))
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Parollar bir xil emas."))
        return password2

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'description', 'requirements', 'experience_level', 'job_type', 'location_type', 'location', 'salary', 'tags']
        labels = {
            'title': _('Lavozim nomi'),
            'description': _('Tavsif'),
            'requirements': _('Talablar'),
            'experience_level': _('Tajriba darajasi'),
            'job_type': _('Ish turi'),
            'location_type': _('Joylashuv turi'),
            'location': _('Joylashuv'),
            'salary': _('Maosh'),
            'tags': _('Teglar'),
        }
        widgets = {
            'tags': forms.TextInput(attrs={'placeholder': _('Teglarni vergul bilan ajrating')}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        labels = {
            'cover_letter': _('Xat'),
            'resume': _('Rezyume'),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'website']
        labels = {
            'name': _('Kompaniya nomi'),
            'description': _('Tavsif'),
            'website': _('Veb-sayt'),
        }

