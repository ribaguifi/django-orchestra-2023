from urllib.parse import urlparse

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def render_email_template(template, context):
    """
    Renders an email template with this format:
        {% if subject %}Subject{% endif %}
        {% if message %}Email body{% endif %}

    context must be a dict
    """
    if not 'site' in context:
        from orchestra import settings
        url = urlparse(settings.ORCHESTRA_SITE_URL)
        context['site'] = {
            'name': settings.ORCHESTRA_SITE_NAME,
            'scheme': url.scheme,
            'domain': url.netloc,
        }
    context['email_part'] = 'subject'
    subject = render_to_string(template, context).strip()
    context['email_part'] = 'message'
    message = render_to_string(template, context).strip()
    return subject, message


def send_email_template(template, context, to, email_from=None, html=None, attachments=[]):
    if isinstance(to, str):
        to = [to]
    subject, message = render_email_template(template, context)
    msg = EmailMultiAlternatives(subject, message, email_from, to, attachments=attachments)
    if html:
        subject, html_message = render_email_template(html, context)
        msg.attach_alternative(html_message, "text/html")
    msg.send()
