from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from .models import Artist, Song, Proposal, Feedback


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'password_confirmation')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        token = Token.objects.create(user=user)
        token.save()

        return user


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'uuid', 'name')


class SongSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(
        queryset=Artist.objects.all(),
        read_only=False,
        slug_field='name',
    )

    featuring_artist = serializers.SlugRelatedField(
        many=True,
        queryset=Artist.objects.all(),
        read_only=False,
        slug_field='name',
        default=[],
    )

    class Meta:
        model = Song
        fields = ('id', 'uuid', 'title', 'artist', 'featuring_artist', 'youtube_url', 'thumbnail_url', 'created_at')
        read_only_fields = ('created_at', )


class ProposalSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        read_only=False,
        slug_field='username',
    )

    class Meta:
        model = Proposal
        fields = ('id', 'uuid', 'youtube_url', 'created_by', 'created_at', 'song_info', 'rejected', 'song', 'updated_at')
        read_only_fields = ('created_at', )


class FeedbackSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        read_only=False,
        slug_field='username',
        required=False,
    )

    class Meta:
        model = Feedback
        fields = ('id', 'uuid', 'comment', 'created_by', 'created_at', 'treated', 'response')
        read_only_fields = ('created_at', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'date_joined',
        )
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')
