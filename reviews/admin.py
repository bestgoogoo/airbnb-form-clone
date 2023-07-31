from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("so", "So"),
            ("fantastic", "Fantastic"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word:
            return reviews.filter(payload__contains=word)
        else:
            return reviews


class RatingFilter(admin.SimpleListFilter):
    title = "Filter by Rating"
    parameter_name = "rating"

    def lookups(self, requet, model_admin):
        return [
            ("under_3", "3⭐️👇"),
            ("over_3", "3⭐️👆"),
        ]

    def queryset(self, request, reviews):
        if self.value() == "under_3":
            return reviews.filter(rating__lt=3)
        else:
            return reviews.filter(rating__gte=3)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "room",
        "experience",
        "payload",
    )

    list_filter = (
        WordFilter,
        RatingFilter,
        "room",
        "user__is_host",
        "room__category",
    )
