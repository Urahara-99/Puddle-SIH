from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from item.models import Class, Domain, Enrollment
from django.db.models import Count, Q

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirect to the appropriate dashboard based on the user’s role
            if user.is_staff:
                return redirect('dashboard:staff_dashboard')
            else:
                return redirect('dashboard:student_dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
def student_dashboard(request):
    user = request.user

    # Get all domains where the user is enrolled
    domains = Domain.objects.filter(classes__enrollment__user=user).distinct()

    # Get all enrollments for the user
    enrollments = Enrollment.objects.filter(user=user).select_related('course', 'course__domain')

    context = {
        'user': user,
        'domains': domains,
        'enrollments': enrollments,
    }

    return render(request, 'dashboard/student_dashboard.html', context)


@login_required
def staff_dashboard(request):
    user = request.user
    
    # Fetch domains uploaded by the staff user
    domains = Domain.objects.filter(classes__created_by=user).distinct()

    context = {
        'domains': domains,
    }

    return render(request, 'dashboard/staff_dashboard.html', context)

@login_required
def domain_detail(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)

    if request.user.is_staff:
        # Staff can see all classes in the domain
        classes = Class.objects.filter(domain=domain)
    else:
        # Students see only classes they're enrolled in within the domain
        classes = Class.objects.filter(
            domain=domain,
            enrollment__user=request.user
        ).distinct()

    return render(request, 'item/domain_detail.html', {
        'domain': domain,
        'classes': classes
    })

@login_required
def enroll_domain(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    user = request.user
    classes = Class.objects.filter(domain=domain)

    for class_instance in classes:
        Enrollment.objects.get_or_create(user=user, course=class_instance)

    return redirect('dashboard:domain_detail', domain_id=domain.id)

def dashboard_view(request):
    user = request.user

    # Get the number of courses for each status
    finished_courses = Enrollment.objects.filter(user=user, status='finished').count()
    ongoing_courses = Enrollment.objects.filter(user=user, status='ongoing').count()
    ended_courses = Enrollment.objects.filter(user=user, status='ended').count()

    # Pass the counts to the template context
    context = {
        'finished_courses': finished_courses,
        'ongoing_courses': ongoing_courses,
        'ended_courses': ended_courses,
    }

    return render(request, 'dashboard/student_dashboard.html', context)

@login_required
def student_enroll_view(request):
    # Fetch all domains
    domains = Domain.objects.all()

    # For each domain, check if the current user is enrolled
    for domain in domains:
        domain.is_enrolled = Enrollment.objects.filter(user=request.user, course__domain=domain).exists()

    context = {
        'domains': domains
    }

    return render(request, 'dashboard/student_enroll.html', context)