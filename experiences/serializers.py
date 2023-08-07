from rest_framework.serializers import ModelSerializer
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from .models import Experience, Content


class ContentSerializer(ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class ExperienceListSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    contents = ContentSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Experience
        fields = "__all__"
