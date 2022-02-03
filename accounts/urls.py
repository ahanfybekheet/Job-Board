from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.sign_up ,name='signup'),
    path('profile/', views.prof,name='profile'),
    path('profile/edit',views.edit_prof,name='edit-profile')
]
