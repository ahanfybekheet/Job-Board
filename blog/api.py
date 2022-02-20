from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from blog.models import Blog
from blog.serializers import BlogSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics









# --------------------------- Using FBV-----------------------------------------------
@api_view(['GET', 'POST'])
def blog_list(request,format=None):
    queryset = Blog.objects.all()
    if request.method == "GET":
        serializer = BlogSerializer(queryset,many=True)
        return Response(serializer.data)
    elif request.method =="POST":
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','DELETE'])
def blog_detail(request,slug,format=None):
    queryset = Blog.objects.get(slug=slug)
    if request.method == 'GET':
        serializer = BlogSerializer(queryset)
        return Response(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = BlogSerializer(instance=queryset,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#--------------------------- Using Primitive CBV--------------------------------------------------
class PBlogList(APIView):
    x = Blog.objects.all()

    def get(self,request):
        serializer = BlogSerializer(self.x,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = BlogSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PBlogDetail(APIView):
    def get_object(self, slug):
        try:
            return Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            raise Http404

    def get(self,*args, **kwargs):
        serializer = BlogSerializer(self.get_object(kwargs['slug']))
        return Response(serializer.data)

    def put(self,*args, **kwargs):
        data = JSONParser().parse(self.request)
        serializer = BlogSerializer(instance=self.get_object(kwargs['slug']),data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,*args, **kwargs):
        self.get_object(kwargs['slug']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#--------------------------- Using Advanced CBV--------------------------------------------------
class BlogList(generics.ListCreateAPIView):
    queryset = Blog.objects
    serializer_class = BlogSerializer

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects
    serializer_class = BlogSerializer
    lookup_field = "slug"

