from rest_framework import serializers

from events.models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source="organizer.username")

    class Meta:
        model = Event
        fields = ("id", "title", "description", "date", "location", "organizer")
        read_only_fields = ("id", "created_at", "updated_at", "organizer")


class ParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = EventRegistration
        fields = ("username", "registered_at")
