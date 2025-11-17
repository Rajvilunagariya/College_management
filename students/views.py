from django.shortcuts import render
from accounts.decorators import student_required

@student_required
def student_profile_view(request):
    # The student profile is accessed via the one-to-one relationship
    profile = request.user.studentprofile
    context = {
        'profile': profile
    }
    return render(request, 'students/student_profile.html', context)
