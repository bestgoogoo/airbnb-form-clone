from django.utils import timezone
from rest_framework import serializers
from experiences.serializers import ExperienceTimeSerializer
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can`t book in the past")
        return value

    def validate(self, data):
        room = self.context.get("room")
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check out should be bigger than Check in"
            )
        if Booking.objects.filter(
            room=room,
            check_in__lt=data["check_out"],
            check_out__gt=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken"
            )
        return data


class PublicRoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "guests",
        )


class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    experience = ExperienceTimeSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "experience",
            "guests",
        )


class PublicExperienceBookingSerializer(serializers.ModelSerializer):
    experience = ExperienceTimeSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "pk",
            "experience",
            "guests",
        )
