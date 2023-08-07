from django.db import models
from common.models import CommonModel


class Experience(CommonModel):
    name = models.CharField(
        max_length=250,
        default="",
    )
    country = models.CharField(
        max_length=50,
        default="Korea",
    )
    city = models.CharField(
        max_length=80,
        default="Seoul",
    )
    price = models.PositiveIntegerField()
    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    contents = models.ManyToManyField(
        "experiences.Content",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )

    def __str__(self) -> str:
        return self.name

    def total_contents(self):
        return self.contents.count()


class Content(CommonModel):

    """What is included on an Experience"""

    name = models.CharField(max_length=100)
    detail = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    explanation = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name
