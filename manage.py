#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
""" importo estas clases para modificar el puerto en el que se ejcutara django """
from django.core.management.commands.runserver import Command as runserver
from django.conf import settings


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mitienda_app.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        """ esta linea usas las clases para cambiar el puerto de django """
    runserver.default_port = settings.RUN_SERVER_PORT
    execute_from_command_line(sys.argv)
    


if __name__ == '__main__':
    main()
