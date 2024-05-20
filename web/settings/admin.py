from django.contrib import admin

from parler.admin import TranslatableStackedInline, TranslatableAdmin

from .models import Page, Seo, Slide, Notification


# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'has_seen', 'is_active', 'priority', 'status', 'created_at', 'updated_at',)
    list_filter = ('has_seen', 'is_active', 'priority', 'status', 'created_at', 'updated_at',)
    search_fields = ('id', 'message', 'user',)


@admin.register(Slide)
class SlideAdmin(TranslatableAdmin):
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
class PageAdmin(TranslatableAdmin):
    list_display = ["id", "type", "created_at", "updated_at", "is_active"]
    list_filter = ["type", "is_active", "created_at", "updated_at"]
    inlines = [SeoStackedInline]
    fieldsets = (
        ('General', {"fields": ('type', 'video', 'video_poster', 'is_active')}),
    )
