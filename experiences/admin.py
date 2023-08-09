from django.contrib import admin
from .models import Experience, Content


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "host",
        "created_at",
    )
    list_filter = (
        "country",
        "city",
        "price",
        "host",
        "date",
        "start",
        "end",
        "contents",
        "created_at",
        "category",
    )


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "detail",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
