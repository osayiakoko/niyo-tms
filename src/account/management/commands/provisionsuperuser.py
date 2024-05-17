from logging import getLogger

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from account.models import User

logger = getLogger(__name__)


class Command(BaseCommand):
    help = "Creates a super user"

    def handle(self, *args, **options):
        try:
            username = settings.SUPERUSER_USERNAME
            password = settings.SUPERUSER_PASSWORD

            if not (username and password):
                raise ValueError("Username or Password not provided")

            superuser_exists: bool = User.objects.filter(
                Q(is_superuser=True) | Q(email=username)
            ).exists()

            if not superuser_exists:
                User.objects.create_superuser(username, password)
                logger.info("Super user created")
        except Exception as e:
            logger.error(f"Error provisioning superuser: {e}")
            raise CommandError(e)
