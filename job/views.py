from django.views.generic import ListView , DetailView , FormView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from accounts.models import profile
from .models import *
from django.shortcuts import redirect ,render
from django.core.paginator import Paginator
from .form import *
from django.contrib.auth.decorators import login_required




#----------------------using fbv------------------------------------------------------------------------------------------------------------
def jobs(request):
    all_jobs = job.objects.all()
    job_filter = filter(request.GET)
    if job_filter.is_valid():
        if job_filter.cleaned_data['title'] != '':
            all_jobs =all_jobs.filter(title__icontains= job_filter.cleaned_data['title'])
        if job_filter.cleaned_data['experince'] != None :
            all_jobs =all_jobs.filter(experince = job_filter.cleaned_data['experince'])
        if job_filter.cleaned_data['salary'] != None :
            all_jobs =all_jobs.filter(salary  = job_filter.cleaned_data['salary'])
        if job_filter.cleaned_data['categorie'] != None :
            all_jobs =all_jobs.filter(categorie=job_filter.cleaned_data['categorie'])
        if job_filter.cleaned_data['job_type'] != '':
            all_jobs =all_jobs.filter(job_type= job_filter.cleaned_data['job_type'])
    paginator = Paginator(all_jobs,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = { 'jobs'          : page_obj,
                'all_jobs'      : all_jobs,
                'filter_form'   : job_filter,
                }
    return render(request,'job/jobs.html',context=context)

#------------------------------ using CBV ----------------------------------------
class JobList(ListView):
    queryset = job.objects.all()
    paginate_by = 2
    template_name ='job/jobs_cbv.html'
    
    def get(self,*args, **kwargs):
        self.form = filter(self.request.GET)
        if self.form.is_valid():
            if self.form.cleaned_data['title'] != '':
                self.queryset =self.queryset.filter(title__icontains= self.form.cleaned_data['title'])
            if self.form.cleaned_data['experince'] != None :
                self.queryset =self.queryset.filter(experince = self.form.cleaned_data['experince'])
            if self.form.cleaned_data['salary'] != None :
                self.queryset =self.queryset.filter(salary  = self.form.cleaned_data['salary'])
            if self.form.cleaned_data['categorie'] != None :
                self.queryset =self.queryset.filter(categorie=self.form.cleaned_data['categorie'])
            if self.form.cleaned_data['job_type'] != '':
                self.queryset =self.queryset.filter(job_type= self.form.cleaned_data['job_type'])
        return super().get(self,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form 
        return context
    


#----------------------using fbv------------------------------------------------------------------------------------------------------------
def job_details(request,slug):
    
    job_detail = job.objects.get(slug=slug)
    if request.method == 'POST':
        apply_form = apply(request.POST,request.FILES)
        if apply_form.is_valid():
            myform = apply_form.save(commit=False)
            myform.job =job_detail
            myform.save()
            return redirect('/')
    else:
        apply_form = apply()

    context = {'job': job_detail,'apply_form':apply_form}
    return render(request,'job/job_details.html',context=context)


class JobDetail(FormMixin,DetailView):
    model = job
    template_name ='job/job_details_cbv.html'
    form_class = apply

    def post(self,*args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return super().post(self,*args, **kwargs)

    def form_valid(self, form):
        myform = form.save(commit=False)
        myform.job = job.objects.get(slug=self.kwargs['slug'])
        myform.save()
        return super().form_valid(form)

    def get_success_url(self) :
        return reverse('JobDetail',kwargs={'slug':self.kwargs['slug']})







#------------------------------ using CBV ----------------------------------------
@login_required
def post_job(request):
    if request.method == 'POST':
        job_form = job_post_form(request.POST,request.FILES)
        if job_form.is_valid():
            myform = job_form.save(commit=False)
            myform.user = request.user
            myform.save()
            job_slug = job.objects.get(title=myform.title)
            return redirect(f'/job-details/{job_slug.slug}')
    else:
        job_form = job_post_form()
    context = {'post_job':job_form}
    return render(request,'job/job_post.html',context)

#------------------------------ using CBV ----------------------------------------
class PostJob(LoginRequiredMixin,FormView):
    form_class = job_post_form
    template_name = "job/job_post_cbv.html"

    def get_success_url(self) -> str:
        return reverse('JobDetail',kwargs={'slug':self.slug})

    def form_valid(self, form):
        myform = form.save(commit=False)
        myform.user = self.request.user
        myform.save()
        self.slug = myform.slug
        return super().form_valid(form)