from rest_framework.serializers import ModelSerializer
from .models import Experience, Content


class ExperienceListSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceDetailSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ContentSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"
