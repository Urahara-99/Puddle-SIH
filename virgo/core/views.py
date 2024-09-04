from django.shortcuts import render, redirect
from item.models import Domain, Class
from .forms import SignupForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login

def index(request):
    # Update the items and categories according to the new models
    classes = Class.objects.all()[:6]
    domains = Domain.objects.all()

    return render(request, 'core/index.html', {
        'classes': classes,
        'domains': domains,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')  # assuming 'user_type' is the field name for the radio buttons

            # Redirect or perform different actions based on user type
            if user_type == 'student':
                return redirect('/student-dashboard/')
            elif user_type == 'faculty':
                return redirect('/staff-dashboard/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'core/login.html'

    def get_success_url(self):
        # Redirect to the appropriate dashboard based on the user’s role
        if self.request.user.is_staff:
            return reverse_lazy('dashboard:staff_dashboard')
        else:
            return reverse_lazy('dashboard:student_dashboard')
