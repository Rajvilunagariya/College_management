# File: accounts/migrations/0002_create_superuser.py

from django.db import migrations
import os

def create_superuser(apps, schema_editor):
    """
    Creates a default superuser for the system.
    """
    CustomUser = apps.get_model('accounts', 'CustomUser')

    # Use environment variables for security, with defaults for development
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'superadmin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'superadmin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass123')

    # Check if the user already exists to prevent errors
    if not CustomUser.objects.filter(username=username).exists():
        print(f"\nCreating superuser '{username}'")
        CustomUser.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            user_type=1  # Set user_type to Admin
        )
    else:
        print(f"\nSuperuser '{username}' already exists. Skipping creation.")


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]