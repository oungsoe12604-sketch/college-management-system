from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('student_list/', views.student_list, name='student_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_student, name='add_student'),
    path('school-info/', views.school_info, name='school_info'),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('create_course/', views.create_course, name='create_course'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('course/<int:id>/', views.course_detail, name='course_detail'),

]

