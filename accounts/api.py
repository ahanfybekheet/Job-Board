from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
from .serializers import *
from .models import *


class ProfileList(ListCreateAPIView):
    model = profile
    serializer_class = ProfileSerializer

class ProfileDetail(RetrieveUpdateDestroyAPIView):
    model = profile
    serializer_class = ProfileSerializer