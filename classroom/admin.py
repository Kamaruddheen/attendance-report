from django.contrib import admin
from .models import *


class ClassroomModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'year', 'sec', 'tutor']
    search_fields = ['course', 'year', ]


admin.site.register(ClassroomModel, ClassroomModelAdmin)
