from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_created_related', null=True,
                                   blank=True, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_updated_related', null=True,
                                   blank=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'updated_at', 'created_at', 'updated_by')

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        obj.save()
