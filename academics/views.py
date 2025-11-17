from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CourseCreationForm

@login_required
def add_course_view(request):
    # Allow access only to Admin (1) and Faculty (2)
    if request.user.user_type not in [1, 2]:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = CourseCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course has been added successfully!")
            # Redirect back to the user's own dashboard
            return redirect('dashboard_redirect')
    else:
        form = CourseCreationForm()
    
    return render(request, 'academics/add_course.html', {'form': form})

