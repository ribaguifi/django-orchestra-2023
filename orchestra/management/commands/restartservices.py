from django.core.management.base import BaseCommand

from orchestra import settings
from orchestra.management.commands.startservices import ManageServiceCommand


class Command(ManageServiceCommand):
    services = settings.ORCHESTRA_RESTART_SERVICES
    action = 'restart'
    help = 'Restart all related services. Usefull for reload configuration and files.'
