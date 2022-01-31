from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from backend.settings import FRONT_APP_URL, EMAIL_HOST_USER


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
        'reset_password_url': "{}/reset_password?token={}".format(
            FRONT_APP_URL,
            reset_password_token.key),
        'app_url': FRONT_APP_URL,
    }

    # render email text
    email_html_message = render_to_string('email/reset_password.html', context)
    email_plaintext_message = render_to_string('email/reset_password.txt', context)

    message = EmailMultiAlternatives(
        # title:
        "{title} 🎤 Réinitialisation de mot de passe".format(title="KaraokeOK"),
        # message:
        email_plaintext_message,
        # from:
        EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    message.attach_alternative(email_html_message, "text/html")
    message.send()
