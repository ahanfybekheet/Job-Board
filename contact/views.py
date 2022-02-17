from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import FormView , DetailView , TemplateView
from .form import ContactForm
# Create your views here.


#--------------------using FBV----------------------------
def contact(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message += f' from: {email} name: {name} '
        send_mail(
            f'(jobboard contact) - > {subject}',
            message,
            settings.EMAIL_HOST_USER,
            ['el.badwy08@gmail.com'],
            fail_silently=False

        )
    return render(request,'contact/contact.html',{})



#-------------------using FormView-------------------------
class Contact1(FormView):
    template_name = 'contact/contact_cbv.html'
    form_class = ContactForm
    success_url = 'contact1'
    def form_valid(self, form):
        message = form.cleaned_data['message']
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message += f'\n from: {email} , name: {name}'
        send_mail(
            f'(jobboard contact) - > {subject}',
            message,
            settings.EMAIL_HOST_USER,
            ['el.badwy08@gmail.com'],
            fail_silently=False

        )
        return super().form_valid(form)



#------------using templateview----------------
class Contact2(TemplateView):
    template_name = 'contact/contact.html'
    def post(self, request, *args, **kwargs):
        message = request.POST.get('message')
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message += f' from: {email} name: {name}'
        send_mail(
            f'(jobboard contact) - > {subject}',
            message,
            settings.EMAIL_HOST_USER,
            ['el.badwy08@gmail.com'],
            fail_silently=False

        )
        return render(request,'contact/contact.html',{})