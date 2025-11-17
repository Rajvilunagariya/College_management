# academics/migrations/0002_populate_departments.py

from django.db import migrations

def create_initial_departments(apps, schema_editor):
    """
    Creates the default departments in the database.
    """
    Department = apps.get_model('academics', 'Department')
    
    # List of departments you want to add by default
    DEPARTMENTS = [
        "Computer Science",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Business Administration",
        "Humanities and Social Sciences",
    ]
    
    for dept_name in DEPARTMENTS:
        # This check prevents creating duplicates if the migration is run again
        if not Department.objects.filter(name=dept_name).exists():
            Department.objects.create(name=dept_name)

class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_departments),
    ]