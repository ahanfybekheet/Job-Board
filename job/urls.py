from django.urls import path
from . import views
from . import api
urlpatterns = [

    #fbv
    path('',views.jobs,name='home'),
    path('job-details/<slug:slug>',views.job_details,name='job-details'),
    path('post-job/',views.post_job,name='post_job'),

    #cbv
    path('cbv/',views.JobList.as_view(),name='JobList'),
    path('cbv/job-details/<slug:slug>',views.JobDetail.as_view(),name='JobDetail'),
    path('cbv/post-job/',views.PostJob.as_view(),name='PostJob'),



    #API
    path('api/',api.JobList.as_view(),name='JobList'),
    path('api/<slug:slug>',api.JobDetail.as_view(),name='JobDetail'),
]
