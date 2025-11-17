from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

admin_required = user_passes_test(lambda u: u.is_authenticated and u.user_type == 1, login_url='/accounts/login/')
faculty_required = user_passes_test(lambda u: u.is_authenticated and u.user_type == 2, login_url='/accounts/login/')
student_required = user_passes_test(lambda u: u.is_authenticated and u.user_type == 3, login_url='/accounts/login/')
