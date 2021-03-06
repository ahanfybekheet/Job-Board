from django.urls import path ,include
from . import views,api



urlpatterns = [
    ## FBV
    path('signup', views.sign_up ,name='signup'),
    path('profile/', views.prof,name='profile'),
    path('profile/edit',views.edit_prof,name='edit-profile'),

    ## CBV
    path('cbv/signup',views.SignUp.as_view(),name="SignUp"),
    path('cbv/profile/', views.Profile.as_view(),name='Profile'),
    path('cbv/profile/edit',views.EditProfile.as_view(),name='EditProfile'),


    ## API
    path('api/cbv/',api.ProfileList.as_view()),
    path('api/cbv/<pk:pk>',api.ProfileDetail.as_view()),

]
