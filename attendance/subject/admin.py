from django.contrib import admin
from .models import SubjectModel, HourModel

# Register your models here.
# admin.site.register(SubjectModel)

class SubjectInline(admin.TabularInline):
	model = SubjectModel
	extra = 1

@admin.register(HourModel)
class HourModelAdmin(admin.ModelAdmin):
	inlines = [
		SubjectInline,
	]

@admin.register(SubjectModel)
class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'sub_name', 'hour', 'handled_by']
    search_fields = ['sub_name', 'hour', ]