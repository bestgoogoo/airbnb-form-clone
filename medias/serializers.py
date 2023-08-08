from rest_framework import serializers
from .models import Photo, Video


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "pk",
            "file",
            "description",
            "created_at",
        )


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            "pk",
            "file",
            "created_at",
        )
