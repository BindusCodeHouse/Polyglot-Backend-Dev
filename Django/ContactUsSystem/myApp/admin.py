from django.contrib import admin
from .models import ContactUs

# Register your models here.
@admin.register(ContactUs)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'subject',
        'message',
        'created_at'
    )
