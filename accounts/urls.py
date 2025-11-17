from django.urls import path
from .views import (
    login_view, 
    logout_view, 
    
    add_student_view, # Admin add student
    add_faculty_view, # Admin add faculty
    register_view, # Import the new registration view
    manage_requests_view, # <-- NEW
    approve_request_view, # <-- NEW
    reject_request_view, # <-- NEW
    dashboard_redirect_view,
    admin_dashboard_view,
    faculty_dashboard_view,
    student_dashboard_view,

    student_list_view,
    faculty_list_view,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-student/', add_student_view, name='add_student'),
    path('add-faculty/', add_faculty_view, name='add_faculty'),
    path('register/', register_view, name='register'), # Add the new public registration URL
    path('requests/', manage_requests_view, name='manage_requests'), # <-- NEW
    path('requests/approve/<int:request_id>/', approve_request_view, name='approve_request'), # <-- NEW
    path('requests/reject/<int:request_id>/', reject_request_view, name='reject_request'), # <-- NEW
    path('dashboard/', dashboard_redirect_view, name='dashboard_redirect'),
    path('dashboard/admin/', admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/faculty/', faculty_dashboard_view, name='faculty_dashboard'),
    path('dashboard/student/', student_dashboard_view, name='student_dashboard'),

    path('students/', student_list_view, name='student_list'),
    path('faculty/', faculty_list_view, name='faculty_list'),
]
