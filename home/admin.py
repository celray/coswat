from django.contrib import admin

from django.contrib import admin
from . import models
from django_summernote.admin import SummernoteModelAdmin


class model_data_src_admin(SummernoteModelAdmin):
    list_display = ('name', 'type', 'version',)
    summernote_fields = '__all__'

admin.site.register(models.model_data, model_data_src_admin)


