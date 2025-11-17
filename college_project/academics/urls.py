from django.urls import path
from .views import add_course_view

urlpatterns = [
    path('add-course/', add_course_view, name='add_course'),
]
