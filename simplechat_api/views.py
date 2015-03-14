from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from simplechat.models import Room, Participant, Message
from simplechat_api.serializers import RoomSerializer, ParticipantSerializer, MessageSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    @list_route()
    def recent_messages(self, request):
        queryset = self.queryset
        from_pk = request.QUERY_PARAMS.get('from_pk', None)
        room_pk = request.QUERY_PARAMS.get('room_pk', None)
        if room_pk is not None:
            queryset = queryset.filter(room__pk=room_pk)
        if from_pk is not None:
            queryset = queryset.filter(pk__gte=from_pk)
        return Response(self.serializer_class(queryset, many=True, context={'request': request}).data)