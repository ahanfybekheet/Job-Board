from django.urls import path
from . import views
from . import api
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    ## FBV
    path('fbv/',views.blog_list,name='blog'),
    path('fbv/<slug:slug>',views.blog_detail,name='blog_detail'),

    ## CBV
    path('cbv/',views.BlogList.as_view(),name='BlogList'),
    path('cbv/<slug:slug>',views.BlogDetail.as_view(),name='BlogDetail'),

    ## API fbv
    path('api/fbv/blogs/',api.blog_list,name='blog_list'),
    path('api/fbv/blogs/<slug:slug>',api.blog_detail,name="blog-detail"),

    ## API Primitive CBV
    path('api/pcbv/blogs/',api.PBlogList.as_view(),name='PBlogList'),
    path('api/pcbv/blogs/<slug:slug>',api.PBlogDetail.as_view(),name="PBlogDetail"),

    ## API Advanced CBV
    path('api/cbv/blogs/',api.BlogList.as_view(),name='BlogList'),
    path('api/cbv/blogs/<slug:slug>',api.BlogDetail.as_view(),name="BlogDetail")

    
]

urlpatterns = format_suffix_patterns(urlpatterns)