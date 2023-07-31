from django.contrib import admin
from .models import Room, Amenity


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "price",
        "kind",
        "total_amenities",
        "created_at",
    )

    list_filter = (
        "price",
        "country",
        "city",
        "kind",
        "rooms",
        "toilets",
        "pet_friendly",
        "amenities",
        "created_at",
        "updated_at",
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
