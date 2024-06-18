from django.core.management.base import BaseCommand
from apps.core.queue_listeners.user_queue_listener import UserQueueListener

class Command(BaseCommand):
    help = 'Launches Listener for user data messages: RabbitMQ'

    def handle(self, *args, **options):
        td = UserQueueListener()
        td.start()
        self.stdout.write("Started User Queue Consumer Thread")
