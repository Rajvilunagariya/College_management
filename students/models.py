from django.db import models
from accounts.models import CustomUser
from academics.models import Course, AcademicSession, Subject

class StudentProfile(models.Model):
    """
    Stores detailed information about a student, linked to their user account.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    enrollment_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, blank=True)
    session = models.ForeignKey(AcademicSession, on_delete=models.DO_NOTHING, null=True, blank=True)
    address = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='student_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Attendance(models.Model):
    """
    Records the attendance status for a student in a specific subject on a given date.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student} - {self.subject} on {self.date}: {status}"

class Result(models.Model):
    """
    Stores the marks or grades for a student in a specific subject.
    """
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    assignment_marks = models.FloatField(default=0)
    exam_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'subject', 'session')

    def __str__(self):
        return f"Result for {self.student} in {self.subject}"

