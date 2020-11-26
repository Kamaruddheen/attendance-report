from django.contrib import admin
from .models import SubjectModel

# Register your models here.
# admin.site.register(SubjectModel)


class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'classroom', 'sub_name', 'hour_name', 'handled_by']
    search_fields = ['sub_name', 'hour_name', ]


admin.site.register(SubjectModel, SubjectModelAdmin)
