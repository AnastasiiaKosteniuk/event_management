from django.db import IntegrityError
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from events.filters import EventFilter
from events.models import Event, EventRegistration
from events.permissions import IsOrganizer
from events.serializers import EventSerializer, ParticipantSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    Event management API.

    - Create, view, update, and delete events.
    - Register/unregister for events.
    - View participants (organizer only).
    """

    queryset = Event.objects.select_related("organizer")
    serializer_class = EventSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_class = EventFilter
    search_fields = ["title", "description", "location"]
    ordering_fields = ["date", "created_at"]
    ordering = ["-date"]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "participants"]:
            return [permissions.IsAuthenticated(), IsOrganizer()]
        else:
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @extend_schema(
        summary="Register for event",
        description=(
            "Register the authenticated user for the selected event.\n"
            "- Organizer cannot register for their own event.\n"
            "- Registration is not allowed for past events.\n"
            "- Each user can register only once."
        ),
        responses={
            201: {"type": "object", "example": {"detail": "Successfully registered for the event."}},
            400: {"type": "object", "example": {"detail": "You are already registered for this event."}},
        },
    )
    @action(detail=True, methods=["post"])
    def register(self, request, pk=None):
        """Register the current user for the event."""
        event = self.get_object()

        if event.organizer == request.user:
            return Response({"detail": "Organizer cannot register for their own event."}, status=400)

        if event.date < timezone.now():
            return Response({"detail": "Cannot register for past events."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            EventRegistration.objects.create(user=request.user, event=event)
            return Response({"detail": "Successfully registered for the event."}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"detail": "You are already registered for this event."}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["delete"])
    def unregister(self, request, pk=None):
        """Unregister the current user from the event."""
        event = self.get_object()
        deleted, _ = EventRegistration.objects.filter(user=request.user, event=event).delete()
        if deleted:
            return Response({"detail": "Successfully unregistered."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You were not registered for this event."}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="List event participants",
        description="Returns a list of participants for the selected event. Only the event organizer has permission to view this.",
        responses={200: ParticipantSerializer(many=True)},
    )
    @action(detail=True, methods=["get"])
    def participants(self, request, pk=None):
        """Get list of participants for the event. Only the event organizer has permission to view this."""
        event = self.get_object()
        registrations = EventRegistration.objects.filter(event=event).select_related("user")
        serializer = ParticipantSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
