from rest_framework import (
    views,
    response,
    permissions,
    exceptions,
    status,
)
from rooms.models import Room
from experiences.models import Experience
from .models import Wishlist
from .serializers import WishlistSerializer


class Wishlists(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        all_wishlists = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            all_wishlists,
            many=True,
            context={"request": request},
        )
        return response.Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)

        if serializer.is_valid():
            wishlist = serializer.save(user=request.user)
            serializer = WishlistSerializer(wishlist)
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)


class WishlistDetail(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            context={"request": request},
        )
        return response.Response(serializer.data)

    def put(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            wishlist = serializer.save()
            serializer = WishlistSerializer(wishlist)
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)

    def delete(self, request, pk):
        wishlist = self.get_object(pk, request.user)
        wishlist.delete()
        return response.Response(status=status.HTTP_200_OK)


class WishlistRoom(views.APIView):
    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise exceptions.NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise exceptions.NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_list(pk, request.user)
        room = self.get_room(room_pk)
        if wishlist.rooms.filter(pk=room.pk).exists():
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)
        return response.Response(status=status.HTTP_200_OK)


class WishlistExperience(views.APIView):
    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise exceptions.NotFound

    def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def put(self, request, pk, experience_pk):
        wishlist = self.get_list(pk, request.user)
        experience = self.get_experience(pk)
        if wishlist.experience.filter(pk=experience.pk).exist():
            wishlist.experience.remove(experience)
        else:
            wishlist.experience.add(experience)
        return response.Response(status=status.HTTP_200_OK)
