from accounts.models import profile
from .models import *
from django.shortcuts import redirect ,render
from django.core.paginator import Paginator
from .form import *
from django.contrib.auth.decorators import login_required







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

def job_details(request,slug):
    
    job_detail = job.objects.get(slug=slug)
    if  request.user.is_authenticated :
        if request.method == 'POST':
            apply_form = apply(request.POST,request.FILES)
            if apply_form.is_valid():
                myform = apply_form.save(commit=False)
                myform.job =job_detail
                myform.save()
                return redirect('/')
        else:
            apply_form = apply()
            
    else:
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

