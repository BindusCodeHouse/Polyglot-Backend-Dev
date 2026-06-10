from .models import ContactUs
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def home(request):
    return render(request,'Html/contactUs.html')

def contact(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to Database
        obj = ContactUs.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        print("Saved ID:", obj.id)

        # Send Email
        send_mail(
            subject=f"Contact Form Message from {name}",
            message=f"""
            Name: {name}
            Email: {email}
            Subject: {subject}
            
            Message:
            {message}
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return render(
            request,
            'Html/contactUs.html',
            {'success': True}
        )

    return render(request, 'Html/contactUs.html')