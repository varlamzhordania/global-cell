from django.contrib import admin
from django.contrib.admin import TabularInline
from django.utils.html import mark_safe
from django.conf import settings
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from parler.admin import TranslatableStackedInline, TranslatableAdmin

from .models import Page, Seo, Slide, Notification, DynamicPage, Media


# Register your models here.

class NotificationResource(resources.ModelResource):
    class Meta:
        model = Notification


class SlideResource(resources.ModelResource):
    class Meta:
        model = Slide


class PageResource(resources.ModelResource):
    class Meta:
        model = Page


@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'message', 'has_seen', 'is_active', 'priority', 'status', 'created_at', 'updated_at',)
    list_filter = ('has_seen', 'is_active', 'priority', 'status', 'created_at', 'updated_at',)
    search_fields = ('id', 'message', 'user',)


@admin.register(Slide)
class SlideAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ['id', 'title', 'short_description', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['id', 'title']
    fieldsets = (
        ('Information', {"fields": ('title', 'short_description')}),
        ('Content', {"fields": ('image',)}),
    )


class SeoStackedInline(TranslatableStackedInline):
    model = Seo
    extra = 1
    max_num = 1
    fieldsets = (
        (None, {"fields": (
            "page", "seo_title", "seo_description", "seo_keywords", "seo_canonical", "seo_is_robots_index",
            "seo_is_robots_follow", "json_ld_data")}),
    )


@admin.register(Page)
class PageAdmin(ImportExportModelAdmin, TranslatableAdmin):
    list_display = ["id", "type", "created_at", "updated_at", "is_active"]
    list_filter = ["type", "is_active", "created_at", "updated_at"]
    inlines = [SeoStackedInline]
    fieldsets = (
        ('General', {"fields": ('type', 'application_file', 'video', 'video_poster', 'is_active')}),
    )


class MediaInlineTabular(admin.TabularInline):
    model = Media
    extra = 1


@admin.register(DynamicPage)
class DynamicPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'url', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    inlines = [MediaInlineTabular]

    def url(self, obj):
        if obj.get_absolute_url():
            return mark_safe(f"<a href='{obj.get_absolute_url()}'>{obj.get_absolute_url()}</a>")
        return None

    url.short_description = 'Page URL'
