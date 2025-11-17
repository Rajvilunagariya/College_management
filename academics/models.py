# File: academics/models.py
# -----------------------------------------------------------------------------
from django.db import models

class AcademicSession(models.Model):
    """
    Stores the academic session years. E.g., 2023-2024.
    """
    session_start_year = models.DateField()
    session_end_year = models.DateField()

    def __str__(self):
        return f"{self.session_start_year.year} to {self.session_end_year.year}"

class Department(models.Model):
    """
    Stores college departments. E.g., Computer Science, Electrical Engineering.
    """
    name = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    """
    Stores courses offered by the college. E.g., B.Tech, BCA.
    """
    name = models.CharField(max_length=120, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    """
    Stores subjects taught in courses. E.g., Data Structures, Web Development.
    """
    name = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # The faculty who teaches this subject might be better handled in a separate allocation model.
    # This keeps the core subject definition clean.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.course.name})"








