# Generated by Django 4.0 on 2022-01-02 15:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('youtube_url', models.CharField(max_length=255)),
                ('thumbnail_url', models.CharField(max_length=2048)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='karaokeok.artist')),
                ('featuring_artist', models.ManyToManyField(blank=True, related_name='featuring_artist', to='karaokeok.Artist')),
            ],
        ),
    ]