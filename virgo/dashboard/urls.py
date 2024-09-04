from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('domain/<int:domain_id>/', views.domain_detail, name='domain_detail'),
    path('enroll/domain/<int:domain_id>/', views.enroll_domain, name='enroll_domain'),  
    
    # other patterns
]
