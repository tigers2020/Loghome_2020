from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        from django.utils.html import escape
        if obj.images:
            url = mark_safe(u'<img src="/media_files/%s" width="250px" />' % escape(obj.images))
        else:
            url = mark_safe(u'<img src="%s" width="250px" />' % escape(settings.NO_IMAGE_URL))

        return url

    image_tag.allow_tags = True
    list_display = ('title', 'category', 'author', 'status', 'create_time', 'update_time', 'image_tag')
    readonly_fields = ('image_tag',)
    exclude = ('author', "update_time",)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Category)
