from django.urls import reverse ,reverse_lazy
from django.shortcuts import redirect, render
from django.views import View
from .form import *
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .models import profile
from django.views.generic import FormView , TemplateView , UpdateView , CreateView
from django.http import HttpResponseRedirect

#----------------------using fbv------------------------------------------------------------------------------------------------------------

def sign_up(request):
    if request.method == 'POST':
        signup_form = signup(request.POST)
        if signup_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')
            signup_form.save()
            user = authenticate(username=username,password = password)
            login(request,user)
            return redirect('/')
    else:
        signup_form = signup()


    return render(request,'accounts/signup.html',{'sign_form':signup_form})

#------------------------------ using CBV ----------------------------------------
class SignUp(CreateView):
    template_name = 'accounts/signup_cbv.html'
    form_class = signup

    def get_success_url(self) -> str:
        return reverse('login')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        form.save()
        authenticate(username=username,password=password)
        return super().form_valid(form)

#------------------------------------------------using fbv------------------------------------------------------------

def prof(request):
    data = profile.objects.get(user= request.user)
    context = {'data':data}
    return render(request,'accounts/profile.html',context)

#------------------------------------------------using CBV------------------------------------------------------------
class Profile(TemplateView):
    template_name = 'accounts/profile_cbv.html'

    def get_queryset(self,*args, **kwargs):
        return profile.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['object'] = self.get_queryset()
        return context

#------------------------------------------------using fbv------------------------------------------------------------
def edit_prof(request):
    data = profile.objects.get(user= request.user)
    if request.method == 'POST':
        profileform = profile_form(request.POST,request.FILES,instance=data)
        userform = user_form(request.POST,instance=request.user)
        if profileform.is_valid() and userform.is_valid():
            profileform.save()
            userform.save()
            return redirect('/accounts/profile')


    else:
        profileform = profile_form(instance=data)
        userform = user_form(instance=request.user)
    context = {"userform":userform,"profileform":profileform}
    return render(request,'accounts/profile-edit.html',context)

#------------------------------------------------using CBV------------------------------------------------------------
class EditProfile(TemplateView):
    template_name = 'accounts/profile-edit_cbv.html'

    def get_queryset(self):
        return profile.objects.get(user = self.request.user)

    def post(self,*args, **kwargs):
        self.profileform = profile_form(self.request.POST,self.request.FILES,instance=profile.objects.get(user= self.request.user))
        self.userform = user_form(self.request.POST,instance=self.request.user)
        if self.profileform.is_valid() and self.userform.is_valid():
            self.profileform.save()
            self.userform.save()
            return HttpResponseRedirect(reverse("Profile"))
        return self.get(self,*args, **kwargs)

    def get(self,*args, **kwargs):
        self.profileform = profile_form(instance=profile.objects.get(user= self.request.user))
        self.userform = user_form(instance=self.request.user)
        return super().get(self,*args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['userform'] = self.userform
        context['profileform'] = self.profileform
        return context