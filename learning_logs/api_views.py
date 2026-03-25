from typing import cast
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Topic, Entry
from .serializers import TopicSerializer, EntrySerializer
    
class TopicListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Topic]:  # type: ignore[override]
        return cast(
            QuerySet[Topic],
            Topic.objects.filter(owner=self.request.user),
        )
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TopicDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Topic]:  # type: ignore[override]
        return Topic.objects.filter(owner=self.request.user)

class EntryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Entry]:  # type: ignore[override]
        return Entry.objects.filter(topic__owner=self.request.user)

    def perform_create(self, serializer):
        topic = serializer.validated_data["topic"]

        if topic.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to add entries to this topic."
            )

        serializer.save()

class EntryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Entry]:  # type: ignore[override]
        return Entry.objects.filter(topic__owner=self.request.user)