from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView
from .models import *
from .serializers import *

class JobList(ListCreateAPIView):
    queryset = job.objects
    serializer_class = JobSerializer

class JobDetail(RetrieveUpdateDestroyAPIView):
    queryset = job.objects
    serializer_class = JobSerializer
    lookup_field = 'slug'