from rest_framework import serializers
from .models import Blog , Comment , Keyword , Category

KEYWORD_CHOICES = tuple([(choice.pk, choice) for choice in Keyword.objects.all()])

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    keyword = KeywordSerializer(many=True,read_only=True)
    author = serializers.CharField(source="author.user.username",required=False)
    blog_comment = CommentSerializer(many=True,required=False)
    category = serializers.CharField()
    
    class Meta:
        model = Blog
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BlogSerializer, self).__init__(*args, **kwargs)
        self.fields['about'].required = False
        self.fields['article'].required = False
        self.fields['author'].required = False
        self.fields['category'].required = False
        self.fields['image'].required = False
        self.fields['keyword'].required = False


