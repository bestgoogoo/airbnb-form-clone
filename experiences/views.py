from rest_framework import (
    views,
    response,
    status,
    exceptions,
    permissions,
)
from .models import Experience, Content
from . import serializers


class Experiences(views.APIView):
    def get(self, requset):
        all_experiences = Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(
            all_experiences,
            many=True,
        )
        return response.Response(serializer.data)

    def post(self, request):
        pass


class ExperienceDetail(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(experience)
        return response.Response(serializer.data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise exceptions.PermissionDenied
        experience.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class Contents(views.APIView):
    def get(self, request):
        all_contents = Content.objects.all()
        serializer = serializers.ContentSerializer(all_contents, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        serializer = serializers.ContentSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            serializer = serializers.ContentSerializer(content)
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)


class ContentDetail(views.APIView):
    def get_object(self, pk):
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        content = self.get_object(pk)
        serializer = serializers.ContentSerializer(content)
        return response.Response(serializer.data)

    def put(self, request, pk):
        content = self.get_object(pk)
        serializer = serializers.ContentSerializer(
            content,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_content = serializers.ContentSerializer(serializer.save())
            return response.Response(updated_content.data)
        else:
            return response.Response(serializer.errors)

    def delete(self, request, pk):
        content = self.get_object(pk)
        content.delete()
        return response.Response(status=HTTP_204_NO_CONTENT)
