import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # Use your actual project name

# Create a Celery application instance
app = Celery('myproject')  # Use your actual project name

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # This will automatically find tasks in 'tasks.py' files in your apps
# myproject/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from leads import consumers  # Import your WebSocket consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/alerts/', consumers.AlertConsumer.as_asgi()),  # WebSocket URL for alerts
        ])
    ),
})
