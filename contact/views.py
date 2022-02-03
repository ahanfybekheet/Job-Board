from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.



def send_message(request):
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
        
    else:
        pass
    return render(request,'contact/contact.html',{})
