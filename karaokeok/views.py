from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.response import Response
from youtube_dl import DownloadError

from . import service
from .filters import CaseInsensitiveOrderingFilter
from .serializers import ArtistSerializer, SongSerializer, RegisterSerializer, UserSerializer, ProposalSerializer, \
    FeedbackSerializer
from .models import Artist, Song, Proposal, Feedback


class ArtistView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    filter_backends = [CaseInsensitiveOrderingFilter, DjangoFilterBackend]
    ordering_fields = ['name']
    ordering = ['name']
    filterset_fields = ['id']


class SongView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = SongSerializer
    queryset = Song.objects.all().prefetch_related('artist', 'featuring_artist')
    filter_backends = [CaseInsensitiveOrderingFilter, DjangoFilterBackend, SearchFilter]
    ordering_fields = ['title', 'created_at', 'artist__name']
    filterset_fields = ['artist', 'featuring_artist']
    search_fields = ['title__unaccent', 'artist__name__unaccent', 'featuring_artist__name__unaccent']


class ProposalView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProposalSerializer
    queryset = Proposal.objects.all()
    ordering_fields = ['created_at']
    filterset_fields = ['created_by', 'rejected', 'song']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.initial_data["song_info"] = service.create_song_info(serializer.initial_data["youtube_url"])
        except DownloadError:
            return Response(
                {"youtube_url": ["On a pas trouvé cette vidéo sur YouTube. Vérifie le lien et réessaie."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.initial_data["song_info"] = service.create_song_info(serializer.initial_data["youtube_url"])
        except DownloadError:
            return Response(
                {"youtube_url": ["On a pas trouvé cette vidéo sur YouTube. Vérifie le lien et réessaie."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class FeedbackView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all().prefetch_related('created_by')
    filterset_fields = ['created_by', 'treated']


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class UserView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username']


class RetrieveCurrentUserView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response(serializer.data)
