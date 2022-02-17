from django.shortcuts import redirect, render , HttpResponseRedirect ,resolve_url
from django.db.models import Q
from .models import *
from .form import TitleSearchForm,CommentForm
from accounts.models import profile
from django.core.paginator import Paginator
import datetime as DT
from django.views.generic import ListView , FormView , TemplateView ,DetailView
from django.views.generic.edit import FormMixin
# Create your views here.





#----------------------using fbv------------------------------------------------------------------------------------------------------------
def blog_list(request):
    blogs = Blog.objects.all()  # 
    search_form = TitleSearchForm(request.GET) #
    category = Category.objects.all() #
    keyword = Keyword.objects.all() #
    to_day = DT.date.today() #
    week_ago = to_day - DT.timedelta(days=7) # get date of week ago to get recent post #
    recent_post = Blog.objects.filter(pub_at__gte=week_ago) #
    if search_form.is_valid(): #
        if search_form.cleaned_data['title']: #
            blogs = Blog.objects.filter(Q(title__icontains=search_form.cleaned_data['title'])) #
    if request.GET.get('category'):
        blogs = Blog.objects.filter(Q(category__in=request.GET.get('category')))
    if request.GET.get('keyword'):
        blogs = Blog.objects.filter(Q(keyword__in=request.GET.get('keyword')))
    paginator = Paginator(blogs,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={'blogs':blogs,"search_form":search_form,"blogs":page_obj,"recent_post":recent_post,"category":category,"keyword":keyword}
    return render(request,'blog/blogs.html',context)


#-------------------------------------------using CBV--------------------------------------------------------------
class BlogList(ListView):
    queryset = Blog.objects.all()
    template_name = 'blog/blogs_cbv.html'

    def get(self,*args,**kwargs):
        if self.request.GET.get('title'):
            self.queryset = Blog.objects.filter(title__icontains=self.request.GET.get('title'))
        if self.request.GET.get('category'):
            self.queryset = Blog.objects.filter(Q(category__in=self.request.GET.get('category')))
        if self.request.GET.get('keyword'):
            self.queryset = Blog.objects.filter(Q(keyword__in=self.request.GET.get('keyword')))
        return super().get(self,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['keyword'] = Keyword.objects.all()
        to_day = DT.date.today() 
        week_ago = to_day - DT.timedelta(days=7) 
        context['recent_post'] = Blog.objects.filter(pub_at__gte=week_ago)
        context['blog_list'] = self.queryset
        return context









def blog_detail(request,slug):
    blog = Blog.objects.get(slug=slug)
    id_this_blog = blog.id
    comments = Comment.objects.filter(post=blog)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            myform = comment_form.save(False)
            myform.owner = profile.objects.get(user=request.user)
            myform.post = blog
            myform.save()
            return redirect(f"/blog/{blog.slug}")
    else:
        comment_form = CommentForm()
    context = {"blog":blog,"comments":comments,"comment_form":comment_form}
    if id_this_blog != 1:    
        prev_blog = Blog.objects.get(id=(id_this_blog-1))
        context["prev_blog"] = prev_blog
    if id_this_blog != Blog.objects.last().id:
        next_blog = Blog.objects.get(id=(id_this_blog+1))
        context["next_blog"] = next_blog
    return render(request,'blog/blog_detail.html',context)


# class BlogDetail(FormMixin,DetailView):
#     queryset = Blog.objects.all()
#     form_class = CommentForm
#     success_url = 'blog_detail'
#     template_name = 'blog/blog_detail_cbv.html'
#     def form_valid(self,form):
#         myform = form.save(commit=False)
#         myform.owner = profile.objects.get(user=self.request.user)
#         myform.post = self.object
#         myform.save()
#         return super().form_valid(form)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["comments"] = Comment.objects.filter(post=self.object)

#         return context
    

