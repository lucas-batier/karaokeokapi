from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .filters import CaseInsensitiveOrderingFilter
from .serializers import ArtistSerializer, SongSerializer, RegisterSerializer
from .models import Artist, Song


class ArtistView(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    filter_backends = [CaseInsensitiveOrderingFilter, DjangoFilterBackend]
    ordering_fields = ['name']
    ordering = ['name']
    filterset_fields = ['id']


class SongView(viewsets.ModelViewSet):
    permission_classes = (AllowAny, )  # @todo remove this
    serializer_class = SongSerializer
    queryset = Song.objects.all().prefetch_related('artist', 'featuring_artist')
    filter_backends = [CaseInsensitiveOrderingFilter, DjangoFilterBackend, SearchFilter]
    ordering_fields = ['title', 'created_at', 'artist__name']
    filterset_fields = ['artist', 'featuring_artist']
    search_fields = ['title', 'artist__name', 'featuring_artist__name']  # add fulltext search by @ key


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
