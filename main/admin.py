from django.contrib import admin
from .models import Reports, Emails, Category, FAQs, Links, Attachments, ReportAttributes

# Register your models here.
admin.site.register(Reports)
admin.site.register(Emails)
admin.site.register(Category)
admin.site.register(FAQs)
admin.site.register(Links)
admin.site.register(Attachments)
admin.site.register(ReportAttributes)
