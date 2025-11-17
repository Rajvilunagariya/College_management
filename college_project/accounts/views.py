from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import LoginForm, StudentCreationForm, FacultyCreationForm, PublicRegistrationForm
from .decorators import admin_required, faculty_required, student_required
# We must import the profile models to create them upon registration
from .models import CustomUser , RegistrationRequest  # <-- IMPORTED CustomUser
from students.models import StudentProfile
from faculty.models import FacultyProfile
from academics.models import Course # <-- IMPORTED Course model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage # Use EmailMessage instead of send_mail
from django.template.loader import render_to_string
from django.conf import settings
import os # Needed to build the file path
from .tasks import send_approval_email_task, send_rejection_email_task
from datetime import timedelta




def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # authenticate() automatically checks if user.is_active is True
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard_redirect')
            else:
                form.add_error(None, "Invalid username or password, or account not yet approved.")
    return render(request, 'accounts/login.html', {'form': form})

# --- NEW PUBLIC REGISTRATION VIEW ---
# def register_view(request):
    
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             # The user_type is now set from the form
#             new_user.user_type = form.cleaned_data['user_type']
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()

#             # Create the corresponding profile
#             if new_user.user_type == '2': # Faculty
#                 FacultyProfile.objects.create(user=new_user)
#             elif new_user.user_type == '3': # Student
#                 StudentProfile.objects.create(user=new_user)

#             messages.success(request, "Registration successful! You can now log in.")
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'accounts/register.html', {'form': form})



def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    if request.method == 'POST':
        form = PublicRegistrationForm(request.POST)
        if form.is_valid():
            # Create a request object instead of a user
            new_request = form.save(commit=False)
            # Hash the password before saving it to the request model
            new_request.password = make_password(form.cleaned_data['password'])
            new_request.save()
            messages.success(request, "Registration successful! Your request is pending admin approval.")
            return redirect('login')
    else:
        form = PublicRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})




# --- NEW AADMIN VIEWS FOR REQUEST MANGEMENT ---
@admin_required
def manage_requests_view(request):
    pending_requests = RegistrationRequest.objects.all().order_by('-created_at')
    return render(request, 'accounts/manage_requests.html', {'requests': pending_requests})
@admin_required
def approve_request_view(request, request_id):
    reg_request = get_object_or_404(RegistrationRequest, id=request_id)
    
    if CustomUser.objects.filter(username=reg_request.username).exists():
        messages.error(request, f"A user with the username '{reg_request.username}' already exists. The redundant request has been deleted.")
        reg_request.delete()
        return redirect('manage_requests')
    
    user = CustomUser.objects.create(
        username=reg_request.username,
        password=reg_request.password,
        email=reg_request.email,
        first_name=reg_request.first_name,
        last_name=reg_request.last_name,
        user_type=reg_request.user_type,
        is_active=True
    )

    if user.user_type == 2:
        FacultyProfile.objects.create(user=user)
    elif user.user_type == 3:
        StudentProfile.objects.create(user=user)
    
      # --- SCHEDULE THE APPROVAL EMAIL ---
    # We will schedule the email to be sent 30 seconds from now.
    # You can change timedelta to minutes=1, hours=1, days=1, etc.
    send_approval_email_task(
        user.username, 
        user.email, 
        schedule=timedelta(seconds=120)
    )
      # --- END SCHEDULING LOGIC ---
    reg_request.delete()
    messages.success(request, f"Request for '{user.username}' approved. An approval email will be sent shortly.")
    return redirect('manage_requests')


    # --- UPDATED EMAIL LOGIC WITH ATTACHMENT ---
    # try:
    #     subject = 'Your Registration has been Approved!'
    #     context = {'username': user.username}
    #     message_body = render_to_string('emails/approval_email.txt', context)

    #     # Create the email message object
    #     email = EmailMessage(
    #         subject,
    #         message_body,
    #         settings.DEFAULT_FROM_EMAIL,
    #         [user.email]
    #     )

    #     # Build the full path to the attachment
    #     attachment_path = os.path.join(settings.BASE_DIR, 'attachments', 'welcome_guide.txt')
        
    #     # Attach the file
    #     email.attach_file(attachment_path)
        
    #     # Send the email
    #     email.send()

    # except Exception as e:
    #     messages.error(request, f"User approved, but failed to send email: {e}")
    # # --- END EMAIL LOGIC ---

    

@admin_required
def reject_request_view(request, request_id):
    reg_request = get_object_or_404(RegistrationRequest, id=request_id)
    
   # --- SCHEDULE THE REJECTION EMAIL ---
    send_rejection_email_task(
        reg_request.username, 
        reg_request.email, 
        schedule=timedelta(seconds=10) # Schedule for 10 seconds from now
    )
    # --- END SCHEDULING LOGIC ---
    
    username = reg_request.username
    reg_request.delete()
    messages.warning(request, f"Request for '{username}' rejected. A rejection email will be sent shortly.")
    return redirect('manage_requests')


    # --- UPDATED EMAIL LOGIC (for consistency) ---
    # try:
    #     subject = 'Your Registration Status'
    #     context = {'username': reg_request.username}
    #     message_body = render_to_string('emails/rejection_email.txt', context)

    #     # Using EmailMessage here too, just without an attachment
    #     email = EmailMessage(
    #         subject,
    #         message_body,
    #         settings.DEFAULT_FROM_EMAIL,
    #         [reg_request.email]
    #     )
    #     email.send()

    # except Exception as e:
    #     messages.error(request, f"Failed to send rejection email: {e}")
    # # --- END EMAIL LOGIC ---
    
    # username = reg_request.username
    # reg_request.delete()
    # messages.warning(request, f"Request for '{username}' has been rejected and a notification email has been sent.")
    # return redirect('manage_requests')




# --- ADMIN-ONLY REGISTRATION VIEWS ---
@admin_required
def add_student_view(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.user_type = 3
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            
            # Create StudentProfile and assign the selected course
            course = form.cleaned_data.get('course')
            StudentProfile.objects.create(user=new_user, course=course)
            
            messages.success(request, f"Student '{new_user.username}' has been created and assigned to {course.name}!")
            return redirect('admin_dashboard')
    else:
        form = StudentCreationForm()
    return render(request, 'accounts/add_student.html', {'form': form})

@admin_required
def add_faculty_view(request):
    if request.method == 'POST':
        form = FacultyCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.user_type = 2  # Set user type to Faculty
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            FacultyProfile.objects.create(user=new_user)
            messages.success(request, f"Faculty '{new_user.username}' has been created successfully!")
            return redirect('admin_dashboard')
    else:
        form = FacultyCreationForm()
    return render(request, 'accounts/add_faculty.html', {'form': form})



def dashboard_redirect_view(request):
    if not request.user.is_authenticated:
         return redirect('login')
    if request.user.user_type == 1:
        return redirect('admin_dashboard')
    elif request.user.user_type == 2:
        return redirect('faculty_dashboard')
    elif request.user.user_type == 3:
        return redirect('student_dashboard')
    else:
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')

@admin_required
def admin_dashboard_view(request):
    student_count = CustomUser.objects.filter(user_type=3, is_active=True).count()
    faculty_count = CustomUser.objects.filter(user_type=2, is_active=True).count()
    course_count = Course.objects.count()
    pending_requests_count = RegistrationRequest.objects.count() # <-- ADDED
    context = {
        'student_count': student_count,
        'faculty_count': faculty_count,
        'course_count': course_count,
        'pending_requests_count': pending_requests_count, # <-- ADDED
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@faculty_required
def faculty_dashboard_view(request):
    return render(request, 'accounts/faculty_dashboard.html')

@student_required
def student_dashboard_view(request):
    course_count = Course.objects.count() # <-- ADDED course count
    context = {
        'course_count': course_count,
    }
    return render(request, 'accounts/student_dashboard.html',context)

