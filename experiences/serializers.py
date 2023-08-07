from rest_framework import serializers
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from .models import Experience, Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class ExperienceListSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    is_host = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "host",
            "is_host",
            "start",
            "end",
            "total_contents",
        )

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user


class ExperienceDetailSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    contents = ContentSerializer(
        read_only=True,
        many=True,
    )
    is_host = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = "__all__"

    def get_is_host(self, experience):
        request = self.context["request"]
        return experience.host == request.user
