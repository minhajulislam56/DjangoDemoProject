from django.contrib import admin
from .models import student_list, file_list, category, quotes, ImageFile

# Register your models here.

class student_list_view(admin.ModelAdmin):
    list_display = [
        '__str__',
        'id',
        'cgpa'
    ]
    class Meta:
        model = student_list


admin.site.register(student_list, student_list_view)

class file_list_view(admin.ModelAdmin):
    list_display = (
        'id',
        'file',
        'remark',
        'timestamp'
    )
    class Meta:
        model = file_list

admin.site.register(file_list, file_list_view)


admin.site.register(category)

class quotes_view(admin.ModelAdmin):
    list_display = (
        'body',
        'category',
        'posted_on'
    )
    class Meta:
        model = quotes

admin.site.register(quotes, quotes_view)

class image_view(admin.ModelAdmin):
    list_display = (
        'id',
        'image'
    )
    class Meta:
        model = ImageFile

admin.site.register(ImageFile, image_view)


#MODIFIED TASKS

from .models import Status
from .forms import StatusForm

class StatusAdmin(admin.ModelAdmin):
    list_display = ['user', '__str__', 'image']
    form = StatusForm
    #class Meta:
        #model = Status

admin.site.register(Status, StatusAdmin)