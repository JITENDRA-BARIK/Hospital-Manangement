import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hospital_management.settings")

application = get_wsgi_application()
git push -u origin <branch>git fetch origin
git pull --rebase origin <branch>
# resolve conflicts if any, then:
git push origin <branch>