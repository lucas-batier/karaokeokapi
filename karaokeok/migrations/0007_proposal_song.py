# Generated by Django 4.0.1 on 2022-02-12 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('karaokeok', '0006_remove_proposal_song'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='song',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='karaokeok.song'),
        ),
    ]
