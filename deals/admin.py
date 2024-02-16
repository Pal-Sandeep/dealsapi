from django.contrib import admin

from deals.models import Deal, DealProject, Project

# Register your models here.

admin.site.register(Deal)
admin.site.register(Project)
admin.site.register(DealProject)
