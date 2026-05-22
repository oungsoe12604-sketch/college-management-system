from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Student, Profile, Course, Enrollment
from .forms import StudentForm, RegisterForm, LoginForm


# =========================
# WELCOME PAGE
# =========================
def welcome(request):
    return render(request, "welcome.html")



def admin_dashboard(request):
    return render(request, "admin_dashboard.html", {
        "total_students": Student.objects.count(),
    })


@login_required 
def dashboard(request): 
    total_student = Student.objects.count() 
    male_student = Student.objects.filter(gender="Male").count() 
    female_student = Student.objects.filter(gender="Female").count() 
    recent_student = Student.objects.all().order_by('-id')[:5] 
    context ={ "total_students":total_student, "male_student": male_student, "female_student": female_student, "recent_student" : recent_student } 
    return render(request,"dashboard.html",context)


# =========================
# STUDENT LIST (PAGINATION)
# =========================
def student_list(request):
    query = request.GET.get('q')

    if query:
        students = Student.objects.filter(name__icontains=query)
    else:
        students = Student.objects.all()

    paginator = Paginator(students, 3)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'students.html', {'students': page_obj})


# =========================
# DASHBOARD (OLD SIMPLE)
# =========================
@login_required
def dashboard(request):
    context = {
        "total_students": Student.objects.count(),
        "male_student": Student.objects.filter(gender="Male").count(),
        "female_student": Student.objects.filter(gender="Female").count(),
        "recent_student": Student.objects.order_by('-id')[:5],
    }
    return render(request, "dashboard.html", context)


# =========================
# ADD STUDENT
# =========================
def add_student(request):
    form = StudentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('welcome')

    return render(request, 'add_student.html', {'form': form})


# =========================
# EDIT STUDENT
# =========================
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    form = StudentForm(request.POST or None, request.FILES or None, instance=student)

    if form.is_valid():
        form.save()
        return redirect('student_list')

    return render(request, 'add_student.html', {'form': form})


# =========================
# DELETE STUDENT
# =========================
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('student_list')


# =========================
# SCHOOL INFO
# =========================
def school_info(request):
    return render(request, 'school_info.html')


# =========================
# REGISTER (FIXED)
# =========================
def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )

            return redirect('login')

    return render(request, 'register.html', {'form': form})


# =========================
# LOGIN (ROLE BASED)
# =========================
def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user:
                login(request, user)

                # STAFF (admin user)
                if user.is_staff:
                    return redirect('dashboard')

                profile = Profile.objects.filter(user=user).first()

                if profile and profile.role == "teacher":
                    return redirect('teacher_dashboard')

                return redirect('student_dashboard')


    return render(request, 'login.html', {'form': form})


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('login')



# =========================
# TEACHER DASHBOARD
# =========================
@login_required
def teacher_dashboard(request):
    courses = Course.objects.filter(teacher=request.user)

    enrollments = Enrollment.objects.filter(
        course__teacher=request.user
    ).select_related('student', 'course')

    return render(request, 'teacher_dashboard.html', {
        'courses': courses,
        'enrollments': enrollments
    })


# =========================
# CREATE COURSE (TEACHER)
# =========================
@login_required
def create_course(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')

        Course.objects.create(
            title=title,
            description=description,
            teacher=request.user
        )

        return redirect('teacher_dashboard')

    return render(request, 'create_course.html')

@staff_member_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html", {
        "total_students": Student.objects.count(),
    })

@login_required
def student_dashboard(request):

    courses = Course.objects.all()

    enrolled = Enrollment.objects.filter(
        student=request.user
    ).select_related('course')

    enrolled_ids = enrolled.values_list('course_id', flat=True)

    return render(request, 'student_dashboard.html', {
        'courses': courses,
        'enrolled_ids': enrolled_ids,
        'enrolled': enrolled,   
    })

#=============Course Detail ===========
#======================================
@login_required
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).exists()

    return render(request, 'course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })


# =========================
# ENROLL COURSE
# =========================
@login_required
def enroll_course(request, course_id):
    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id)

        obj, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course
        )

        if created:
            return JsonResponse({
                "status": "success",
                "message": "Successfully enrolled!"
            })
        else:
            return JsonResponse({
                "status": "exists",
                "message": "Already enrolled!"
            })

    return JsonResponse({"status": "error"})
