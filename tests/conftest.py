import django
from pytest_factoryboy import register

def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'dummy_db'
            }
        },
        SECRET_KEY = 'unnecessery',
        ROOT_URLCONF = 'tests.app.urls',
        MIDDLEWARE = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'rest_framework',
            'resource_permissions',
            'tests.app'
        )
    )

    django.setup()

    from tests.app.factories import UserFactory, OfficeFactory, IssueFactory
    register(UserFactory)
    register(OfficeFactory)
    register(IssueFactory)