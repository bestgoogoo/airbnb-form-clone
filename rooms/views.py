from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from .serializers import AmenitySerializer
from .models import Amenity


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializers = AmenitySerializer(all_amenities, many=True)
        return Response(serializers.data)

    def post(slef, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = AmenitySerializer(serializer.save())
            return Response(amenity.data)
        else:
            return Response(serializer.errors)


class AmenityDetial(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = AmenitySerializer(serializer.save())
            return Response(updated_amenity.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
