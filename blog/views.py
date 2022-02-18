from django.shortcuts import redirect , render ,resolve_url
from django.db.models import Q
from .models import *
from .form import TitleSearchForm,CommentForm
from accounts.models import profile
from django.core.paginator import Paginator
import datetime as DT
from django.views.generic import ListView , FormView , TemplateView ,DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse





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
            blogs = Blog.objects.filter(title__icontains=search_form.cleaned_data['title'])#
    if request.GET.get('category'):
        blogs = Blog.objects.filter(category__in=request.GET.get('category'))
    if request.GET.get('keyword'):
        blogs = Blog.objects.filter(keyword__in=request.GET.get('keyword'))
    paginator = Paginator(blogs,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={'blogs':blogs,"search_form":search_form,"blogs":page_obj,"recent_post":recent_post,"category":category,"keyword":keyword}
    return render(request,'blog/blogs.html',context)


#-------------------------------------------using CBV--------------------------------------------------------------
class BlogList(ListView):
    queryset = Blog.objects.all()
    template_name = 'blog/blogs_cbv.html'
    paginate_by = 1
    def get(self,*args,**kwargs):
        if self.request.GET.get('title'):
            self.queryset = Blog.objects.filter(title__icontains=self.request.GET.get('title'))
        if self.request.GET.get('category'):
            self.queryset = Blog.objects.filter(category__in=self.request.GET.get('category'))
        if self.request.GET.get('keyword'):
            self.queryset = Blog.objects.filter(keyword__in=self.request.GET.get('keyword'))
        return super().get(self,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['keyword'] = Keyword.objects.all()
        to_day = DT.date.today() 
        week_ago = to_day - DT.timedelta(days=7) 
        context['recent_post'] = Blog.objects.filter(pub_at__gte=week_ago)
        return context








#----------------------using fbv------------------------------------------------------------------------------------------------------------
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




#------------------------------ using CBV ----------------------------------------
class BlogDetail(FormMixin,DetailView):
    model = Blog
    form_class = CommentForm
    template_name = 'blog/blog_detail_cbv.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.object) 
        try:
            context["prev_blog"] = self.prev_blog
        except:
            pass
        try:
            context["next_blog"] = self.next_blog
        except:
            pass
        return context
    
    def post(self,*args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return super().post(self,*args, **kwargs)

    def form_valid(self,form):
        myform = form.save(commit=False)
        myform.owner = profile.objects.get(user=self.request.user)
        myform.post = Blog.objects.get(slug=self.kwargs['slug'])
        myform.save()
        return super().form_valid(form)

    def get(self,*args, **kwargs):
        self.object = self.get_object()
        id = self.object.id
        if id != 1:    
            self.prev_blog = Blog.objects.get(id=(id-1))
        if id != Blog.objects.last().id:
            self.next_blog = Blog.objects.get(id=(id+1))
        return super().get(self,*args, **kwargs)
    
    def get_success_url(self,*args, **kwargs):
        return reverse("BlogDetail", kwargs={"slug": self.kwargs['slug']})
