from rest_framework import serializers
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist
from .models import Amenity, Room


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    photos = PhotoSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user

    def get_is_liked(self, room):
        request = self.context["request"]
        return Wishlist.objects.filter(
            user=request.user,
            rooms__pk=room.pk,
        ).exists()


class RoomListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]
        return room.owner == request.user
