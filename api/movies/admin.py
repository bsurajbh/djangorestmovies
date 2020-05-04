from django.contrib import admin
from common.base import BaseAdmin
from .models import Movies, UserFeedback


class MovieAdmin(BaseAdmin):
    list_display = ('name', 'year', 'created_at', 'created_by', 'updated_at', 'updated_by')
    search_fields = ('name',)
    list_filter = ('year',)


class UserFeedbackAdmin(BaseAdmin):
    list_display = ('movie', 'rating', 'comment', 'created_at', 'created_by', 'updated_at', 'updated_by')
    search_fields = ('comment', 'movie')
    list_filter = ('movie',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserFeedbackAdmin, self).get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['movie'].queryset = Movies.objects.exclude(movies_feedback__created_by=request.user)
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('movie',)
        return self.readonly_fields


admin.site.register(Movies, MovieAdmin)
admin.site.register(UserFeedback, UserFeedbackAdmin)
