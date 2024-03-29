#!/usr/bin/env python
# INCASE "port is already in use" -> sudo lsof -t -i tcp:8000 | xargs kill -9

# TO RUN THROUGH DOCKER
# docker run --publish 8000:8000 angadsinghsandhu/trends

"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trends.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
