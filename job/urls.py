from django.urls import path
from . import views

urlpatterns = [
    path('',views.jobs,name='home'),
    path('job-details/<slug:slug>',views.job_details,name='job-details'),
    path('post-job/',views.post_job,name='post_job')
]
