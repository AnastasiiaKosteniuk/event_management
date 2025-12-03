from rest_framework import viewsets, permissions

from events.models import Event
from events.permissions import IsOrganizer
from events.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("organizer").order_by("-date")
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            # updating/deleting - only organizer + authenticated
            return [permissions.IsAuthenticated(), IsOrganizer()]
        else:
            # viewing/creating events - any authenticated user
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
