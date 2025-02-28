from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_jobs, name='search_jobs'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-job/', views.create_job, name='create_job'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('signup/', views.signup, name='signup'),
    path('create-company/', views.create_company, name='create_company'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
]

