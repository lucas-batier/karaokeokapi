from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from django_rest_passwordreset.signals import reset_password_token_created
from youtube_dl import DownloadError

from backend.settings import FRONT_APP_URL, EMAIL_HOST_USER, APP_URL
from karaokeok import service
from karaokeok.models import Feedback, Proposal


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'first_name': reset_password_token.user.first_name,
        'reset_password_url': "{}/reset_password{}".format(
            FRONT_APP_URL,
            reset_password_token.key),
        'front_app_url': FRONT_APP_URL,
        'app_url': APP_URL,
    }

    # render email text
    email_html_message = render_to_string('email/reset_password.html', context)
    email_plaintext_message = render_to_string('email/reset_password.txt', context)

    message = EmailMultiAlternatives(
        subject="Réinitialisation mot de passe - {title} 🎤".format(title="KaraokeOK"),
        body=email_plaintext_message,
        from_email='Fred de KaraokeOK',
        to=[reset_password_token.user.email]
    )
    message.attach_alternative(email_html_message, "text/html")
    message.send()


@receiver(post_save, sender=Feedback)
def create_feedback(sender, instance, *args, **kwargs):
    """
    Send an email to the superuser while a user submit a feedback
    :type sender: Feedback
    :type instance: Feedback
    """
    # send an e-mail to the superuser
    context = {
        'first_name': instance.created_by.first_name if instance.created_by else 'Un utilisateur inconnu',
        'last_name': instance.created_by.last_name if instance.created_by else '',
        'username': instance.created_by.username if instance.created_by else '',
        'uuid': instance.uuid,
        'comment': instance.comment,
        'date': instance.created_at,
    }

    # render email text
    email_html_message = render_to_string('email/feedback.html', context)
    email_plaintext_message = render_to_string('email/feedback.txt', context)

    message = EmailMultiAlternatives(
        subject="Avis reçu".format(title="KaraokeOK"),
        body=email_plaintext_message,
        from_email='KaraokeOK admin',
        to=User.objects.filter(is_superuser=True).values_list('email')[0]
    )
    message.attach_alternative(email_html_message, "text/html")
    message.send()


@receiver(post_save, sender=Proposal)
def create_proposal(sender, instance, *args, **kwargs):
    """
    Send an email to the superuser while a user submit a proposal
    :type sender: Proposal
    :type instance: Proposal
    """
    youtube_info = service.fetch_youtube_info(instance.youtube_url)

    artist = youtube_info.get("artist", '')
    title = youtube_info.get("title", '')
    youtube_url = 'https://www.youtube.com/watch?v=%s' % youtube_info.get("id", '')
    thumbnail_url = service.fetch_genius_thumbnail_url(title, artist)

    if youtube_info:
        song_body = '''
            {
                "artist": "%(artist)s",
                "title": "%(title)s",
                "featuring_artist": [],
                "youtube_url": "%(youtube_url)s",
                "thumbnail_url": "%(thumbnail_url)s"
            }
        ''' % {
            "artist": artist,
            "title": title,
            "youtube_url": youtube_url,
            "thumbnail_url": thumbnail_url,
        }
    else:
        song_body = 'Not found on YouTube'

    # send an e-mail to the superuser
    context = {
        'first_name': instance.created_by.first_name,
        'last_name': instance.created_by.last_name,
        'username': instance.created_by.username,
        'uuid': instance.uuid,
        'youtube_url': instance.youtube_url,
        'date': instance.created_at,
        'song_body': song_body,
    }

    # render email text
    email_html_message = render_to_string('email/proposal.html', context)
    email_plaintext_message = render_to_string('email/proposal.txt', context)

    message = EmailMultiAlternatives(
        subject="Proposition reçu".format(title="KaraokeOK"),
        body=email_plaintext_message,
        from_email='KaraokeOK admin',
        to=User.objects.filter(is_superuser=True).values_list('email')[0]
    )
    message.attach_alternative(email_html_message, "text/html")
    message.send()
