
# -----------------------------------------------------------------------------
# File: faculty/models.py
# -----------------------------------------------------------------------------
from django.db import models
from accounts.models import CustomUser
from academics.models import Department, Subject, Course, AcademicSession

class FacultyProfile(models.Model):
    """
    Stores detailed information about a faculty member, linked to their user account.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='faculty_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class SubjectAllocation(models.Model):
    """
    Maps which faculty teaches which subject in a given course and session.
    """
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('faculty', 'subject', 'course', 'session')

    def __str__(self):
        return f"{self.faculty} -> {self.subject} ({self.course})"





