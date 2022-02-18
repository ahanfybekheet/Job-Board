from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.sign_up ,name='signup'),
    path('profile/', views.prof,name='profile'),
    path('profile/edit',views.edit_prof,name='edit-profile'),

    ## CBV
    path('cbv/signup',views.SignUp.as_view(),name="SignUp"),
    path('cbv/profile/', views.Profile.as_view(),name='Profile'),
    path('cbv/profile/edit',views.EditProfile.as_view(),name='EditProfile'),


]
