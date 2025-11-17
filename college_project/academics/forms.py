from django import forms
from academics.models import Course

class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
