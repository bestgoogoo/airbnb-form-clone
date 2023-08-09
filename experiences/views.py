from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import (
    views,
    response,
    status,
    exceptions,
    permissions,
)
from categories.models import Category
from bookings.models import Booking
from medias.serializers import (
    PhotoSerializer,
    VideoSerializer,
)
from bookings.serializers import (
    PublicExperienceBookingSerializer,
    CreateExperienceBookingSerializer,
)
from .models import Experience, Content
from .serializers import (
    ExperienceDetailSerializer,
    ExperienceListSerializer,
    ContentSerializer,
)


class Experiences(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(
            all_experiences,
            many=True,
            context={"request": request},
        )
        return response.Response(serializer.data)

    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise exceptions.ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise exceptions.ParseError("Category kind should be 'Experiences'")
            except Category.DoesNotExist:
                raise exceptions.ParseError("Category not found")
            try:
                with transaction.atomic():
                    experience = serializer.save(
                        host=request.user,
                        category=category,
                    )
                    contents = request.data.get("contents")
                    for content_pk in contents:
                        content = Content.objects.get(pk=content_pk)
                        experience.contents.add(content)
                    serializer = ExperienceDetailSerializer(
                        experience,
                        context={"request": request},
                    )
                    return response.Response(serializer.data)
            except Exception:
                raise exceptions.ParseError("Content not found")
        else:
            return response.Response(serializer.errors)


class ExperienceDetail(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(
            experience,
            context={"request": request},
        )
        return response.Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise exceptions.PermissionDenied
        serializer = ExperienceDetailSerializer(
            experience,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise exceptions.ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise exceptions.ParseError("Category kind should be 'Experiences'")
            except Category.DoesNotExist:
                raise exceptions.ParseError("Category not found")
            try:
                with transaction.atomic():
                    experience = serializer.save(category=category)
                    contents = request.data.get("contents")
                    experience.contents.clear()
                    for content_pk in contents:
                        content = Content.objects.get(pk=content_pk)
                        experience.contents.add(content)
                    updated_experience = ExperienceDetailSerializer(
                        experience,
                        context={"request": request},
                    )
                    return response.Response(updated_experience.data)
            except Content.DoesNotExist:
                raise exceptions.ParseError("Content not found")

    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise exceptions.PermissionDenied
        experience.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class Contents(views.APIView):
    def get(self, request):
        all_contents = Content.objects.all()
        serializer = ContentSerializer(all_contents, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.save()
            serializer = ContentSerializer(content)
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
        serializer = ContentSerializer(content)
        return response.Response(serializer.data)

    def put(self, request, pk):
        content = self.get_object(pk)
        serializer = ContentSerializer(
            content,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_content = ContentSerializer(serializer.save())
            return response.Response(updated_content.data)
        else:
            return response.Response(serializer.errors)

    def delete(self, request, pk):
        content = self.get_object(pk)
        content.delete()
        return response.Response(status=HTTP_204_NO_CONTENT)


class ExperienceContent(views.APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        offset = (page - 1) * page_size
        limit = offset + page_size
        experience = self.get_object(pk)
        serializer = ContentSerializer(experience.contents.all(), many=True)
        return response.Response(serializer.data)


class ExperiencePhotos(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise exceptions.PermissionDenied

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(experience=experience)
            serializer = PhotoSerializer(photo)
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)


class ExperienceVideo(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def post(self, request, pk):
        experience = self.get_object(pk=pk)
        if request.user != experience.host:
            raise exceptions.PermissionDenied

        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save(experience=experience)
            serializer = VideoSerializer(video)
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)


class ExperienceBookings(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
        )
        serializer = PublicExperienceBookingSerializer(bookings, many=True)
        return response.Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        serializer = CreateExperienceBookingSerializer(data=request.data)
        if serializer.is_valid():
            if experience.date <= now:
                raise exceptions.ParseError("Past event cannot be booked")
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicExperienceBookingSerializer(booking)
            return response.Response(serializer.data)
        else:
            return response.Response(serializer.errors)
