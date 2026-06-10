# Contact Us Form with Email Notification (Django)

## Overview

This feature allows users to:

* Submit a Contact Us form.
* Store submitted details in the database.
* Send an email notification to the website administrator.
* Display a success message after successful submission.

---

## Features

✅ Save contact form data into the database.

✅ Send email notifications using Gmail SMTP.

✅ Display success confirmation after form submission.

✅ Easy integration with any Django project.

---

## Technologies Used

* Python
* Django
* Gmail SMTP
* HTML
* CSS
* SQLite/MySQL (Optional)

---

## Project Structure

```text
project/
│
├── app/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── Html/
│           └── contactUs.html
│
└── settings.py
```

---

## Database Model

```python
class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
```

---

## Email Configuration

Add the following configuration in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'yourgmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your_16_character_app_password'
```

### Gmail Setup

1. Enable Two-Factor Authentication (2FA).
2. Open Google Account Security Settings.
3. Navigate to App Passwords.
4. Generate a new App Password.
5. Copy the generated 16-character password.
6. Use it as `EMAIL_HOST_PASSWORD`.

---

## View Implementation

```python
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from .models import ContactUs


def contact(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactUs.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

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
```

---

## How It Works

1. User fills out the Contact Us form.
2. Form data is submitted using POST.
3. Data is saved to the database.
4. Django sends an email notification to the administrator.
5. User receives a success message on the webpage.

---

## Email Notification Format

```text
Subject: Contact Form Message from John Doe

Name: John Doe
Email: john@example.com
Subject: Inquiry

Message:
I would like more information about your services.
```

---

## Testing

Run the Django server:

```bash
python manage.py runserver
```

Submit the contact form and verify:

* Data is stored in the database.
* Email is received in the configured Gmail account.
* Success message appears on the Contact Us page.

---

## Future Enhancements

* Email template with HTML formatting.
* Auto-reply email to users.
* AJAX form submission.
* Toast notification messages.
* Google reCAPTCHA integration.
* Admin dashboard for contact requests.

---

## Author

Developed using Django and Gmail SMTP integration for Contact Us form management and email notifications.
