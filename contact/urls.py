from django.urls import path
from . import views

urlpatterns = [
    ## FBV
    path('fbv',views.contact,name='contact0'),
    ## CBV
    path('cbv1',views.Contact1.as_view(),name='contact1'),
    ## OR
    path('cbv2',views.Contact2.as_view(),name='contact2')
]
