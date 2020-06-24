from django.contrib import admin

from Gallery import models
from import_export.admin import ImportExportModelAdmin


# Register your models here.


def apply_to_publish(modeladmin, request, queryset):
    for instance in queryset:
        if instance.status:
            instance.status = False
        else:
            instance.status = True
        instance.save()
    apply_to_publish.short_description = "publish image"


class ProviderAdmin(admin.ModelAdmin):
    ordering = ('-name',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", 'location', 'provider', 'project_date', 'status',)
    ordering = ('-project_date',)
    list_filter = ('provider',)
    autocomplete_fields = ['location']
    exclude = ('slug',)
    actions = [apply_to_publish, ]


class ImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'image_tag', 'date_taken', 'description', 'status')
    ordering = ('-date_taken',)
    list_filter = ('project',)
    actions = [apply_to_publish, ]


class LocationAdmin(ImportExportModelAdmin):
    list_display = ('state_code', 'state_name')
    ordering = ('-state_code',)

class CityAdmin(ImportExportModelAdmin):
    list_display = ('id_state', 'city', 'country', 'lat', 'lng')
    search_fields = ['city', 'country']
    ordering = ('-id_state',)


admin.site.register(models.City, CityAdmin)
admin.site.register(models.Provider, ProviderAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.HomeImage, ImageAdmin)
admin.site.register(models.Location, LocationAdmin)
