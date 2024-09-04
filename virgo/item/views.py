from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from .forms import NewItemForm, ResourceForm, EditItemForm
from .models import Class, Resource, Enrollment, Domain, Skill, LearningPath
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

@login_required
def new_class(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST)
        resource_forms = [ResourceForm(request.POST, request.FILES, prefix=f'resource_{i}') for i in range(4)]

        if form.is_valid():
            class_instance = form.save(commit=False)
            class_instance.created_by = request.user
            class_instance.save()

            for resource_form in resource_forms:
                if resource_form.is_valid() and resource_form.cleaned_data:
                    resource = resource_form.save(commit=False)
                    resource.class_instance = class_instance
                    resource.save()

            return redirect('item:class_detail', pk=class_instance.id)
    else:
        form = NewItemForm()
        resource_forms = [ResourceForm(prefix=f'resource_{i}') for i in range(4)]

    return render(request, 'item/form.html', {
        'form': form,
        'resource_forms': resource_forms,
        'title': 'New Class',
    })

@login_required
def edit_class(request, pk):
    class_instance = get_object_or_404(Class, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, instance=class_instance)
        resource_forms = [
            ResourceForm(request.POST, request.FILES, prefix=f'resource_{i}', instance=resource)
            for i, resource in enumerate(class_instance.resources.all())
        ]

        if form.is_valid():
            form.save()

            for resource_form in resource_forms:
                if resource_form.is_valid() and resource_form.cleaned_data:
                    resource_form.save()

            return redirect('item:class_detail', pk=class_instance.id)
    else:
        form = EditItemForm(instance=class_instance)
        resource_forms = [
            ResourceForm(instance=resource, prefix=f'resource_{i}')
            for i, resource in enumerate(class_instance.resources.all())
        ]

    return render(request, 'item/form.html', {
        'form': form,
        'resource_forms': resource_forms,
        'title': 'Edit Class',
    })

@login_required
def class_detail(request, pk):
    class_instance = get_object_or_404(Class, pk=pk)

    # Check if the user is enrolled
    user_enrolled = Enrollment.objects.filter(user=request.user, course=class_instance).exists()

    return render(request, 'item/detail.html', {
        'item': class_instance,
        'user_enrolled': user_enrolled,
    })

@login_required
def enroll_in_class(request, class_id):
    class_to_enroll = get_object_or_404(Class, id=class_id)
    user = request.user

    # Check if the user is already enrolled in this class
    enrollment, created = Enrollment.objects.get_or_create(user=user, course=class_to_enroll)

    if created:
        # Record the enrollment start time
        enrollment.start_time = datetime.now()
        enrollment.save()

    return redirect('progress_page')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def progress_page(request):
    if request.user.is_staff:
        domains = Domain.objects.filter(classes__created_by=request.user).distinct()
        enrollments = Enrollment.objects.filter(course__domain__in=domains).select_related('user')
    else:
        classes = Class.objects.filter(enrollment__user=request.user).distinct()
        domains = Domain.objects.filter(classes__in=classes).distinct()
        enrollments = Enrollment.objects.filter(user=request.user).select_related('course')

    
    return render(request, 'item/progress.html', {
        'enrollments': enrollments,
        'domains': domains,
        'classes': classes if not request.user.is_staff else None,
    })

def start_progress(request, class_id):
    user = request.user
    class_instance = Class.objects.get(id=class_id)
    enrollment, created = Enrollment.objects.get_or_create(user=user, course=class_instance)
    if created:
        enrollment.start_time = timezone.now()
        enrollment.save()
    return redirect('progress_page')

def finish_progress(request, class_id):
    user = request.user
    class_instance = get_object_or_404(Class, id=class_id)
    enrollment = get_object_or_404(Enrollment, user=user, course=class_instance)
    
    if enrollment:
        enrollment.end_time = timezone.now()
        enrollment.save()
    
    # Redirect to the correct view
    return redirect('dashboard:student_dashboard')



@login_required
def delete_class(request, pk):
    class_instance = get_object_or_404(Class, pk=pk, created_by=request.user)
    if request.method == 'POST':
        class_instance.delete()
        return redirect('item:items')
    return render(request, 'item/confirm_delete.html', {
        'item': class_instance,
    })

def class_list(request):
    query = request.GET.get('query', '')
    domain_id = request.GET.get('domain', 0)
    domains = Domain.objects.all()
    classes = Class.objects.all()

    # Filter by domain if selected
    if domain_id and int(domain_id) != 0:
        classes = classes.filter(domain_id=domain_id)

    # Filter by search query
    if query:
       classes = classes.filter(Q(class_name__icontains(query)) | Q(description__icontains(query)))

    return render(request, 'item/items.html', {
        'items': classes,
        'query': query,
        'domains': domains,
        'domain_id': int(domain_id),
    })

@login_required
def student_dashboard(request):
    user = request.user
    domains = Domain.objects.all()
    
    if request.user.is_anonymous:
        return HttpResponse("User is not authenticated")

    classes = Class.objects.filter(created_by=request.user)

    for domain in domains:
        domain.is_enrolled = Enrollment.objects.filter(user=user, course__domain=domain).exists()

    context = {
        'domains': domains,
    }
    return render(request, 'dashboard/dashboard.html', context)

    

@login_required
def learning_path_detail(request, pk):
    learning_path = get_object_or_404(LearningPath, pk=pk)
    skills = Skill.objects.filter(learning_paths=learning_path)

    return render(request, 'item/learning_path_detail.html', {
        'learning_path': learning_path,
        'skills': skills,
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST)
        resource_forms = [ResourceForm(request.POST, request.FILES, prefix=f'resource_{i}') for i in range(4)]

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            for resource_form in resource_forms:
                if resource_form.is_valid() and resource_form.cleaned_data:
                    resource = resource_form.save(commit=False)
                    resource.class_instance = item
                    resource.save()

            return redirect('item:class_detail', pk=item.id)
    else:
        form = NewItemForm()
        resource_forms = [ResourceForm(prefix=f'resource_{i}') for i in range(4)]

    return render(request, 'item/form.html', {
        'form': form,
        'resource_forms': resource_forms,
        'title': 'New Item',
    })

def items(request):
    item_list = Domain.objects.all()
    return render(request, 'item/items.html', {'items': item_list})

@login_required
def domain_detail(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    is_enrolled = Enrollment.objects.filter(course__domain=domain, user=request.user).exists()
    classes = domain.classes.order_by('class_name') 
    total_classes = domain.get_total_classes()
    progress_percentage = domain.get_progress_percentage(request.user)


    class_positions = []
    for index, class_item in enumerate(classes):
        position_percentage = (index / total_classes) * 100
        class_positions.append({
            'class_name': class_item.class_name,
            'position_percentage': position_percentage
        })
    
    context = {
        'domain': domain,
        'is_enrolled': is_enrolled,
        'classes': classes,
         'class_positions': class_positions,
        'progress_percentage': progress_percentage,
        'total_classes': total_classes,
    }
    return render(request, 'item/domain_detail.html', context)

@csrf_exempt
@login_required
def enroll_domain(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    user = request.user
    first_class = domain.classes.first()

    # Check if the user is already enrolled
    if not Enrollment.objects.filter(course__domain=domain, user=user).exists():
        if first_class:
            enrollment = Enrollment.objects.create(user=user, course=first_class)
            # Record the enrollment start time
            enrollment.start_time = datetime.now()
            enrollment.save()
            return JsonResponse({'status': 'enrolled', 'enrollment_status': '✔ Enrolled/Progressing'})

    return JsonResponse({'status': 'already_enrolled', 'enrollment_status': '✔ Enrolled/Progressing'})

