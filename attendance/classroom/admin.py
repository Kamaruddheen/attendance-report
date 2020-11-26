from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(ClassroomModel)


class ClassroomModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'year', 'sec', 'tutor']
    search_fields = ['course', 'year', ]


admin.site.register(ClassroomModel, ClassroomModelAdmin)
