from django.urls import path
from . import views
urlpatterns = [
    ## FBV
    path('fbv/',views.blog_list,name='blog'),
    path('fbv/<slug:slug>',views.blog_detail,name='blog_detail'),

    ## CBV
    path('cbv/',views.BlogList.as_view(),name='BlogList'),
    path('cbv/<slug:slug>',views.BlogDetail.as_view(),name='BlogDetail')
]
