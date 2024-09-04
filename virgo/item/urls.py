from django.urls import path
from . import views

app_name = "item"

urlpatterns = [
    path("new/", views.new, name="new"),
    path("", views.items, name="items"),
    path('items/', views.items, name='items'),  # Ensure 'items' view is defined
    path("<int:pk>/edit/", views.edit_class, name="edit"),
    path("new/", views.new, name="new"),
    path('inbox/<int:pk>/', views.inbox, name='inbox'),
    path("class_detail/<int:pk>/", views.class_detail, name="class_detail"),
    path("enroll/<int:course_id>/", views.enroll_in_class, name="enroll_in_class"),
    path('progress/', views.progress_page, name='progress_page'),
    path('progress/start/<int:class_id>/', views.start_progress, name='start_progress'),
    path('progress/finish/<int:class_id>/', views.finish_progress, name='finish_progress'),
    path("delete/<int:pk>/", views.delete_class, name="delete"),
    path("items/", views.items, name="items"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path('domain/<int:domain_id>/', views.domain_detail, name='domain_detail'),
    path('enroll_domain/<int:domain_id>/', views.enroll_domain, name='enroll_domain'),
    path('enroll/<int:class_id>/', views.enroll_in_class, name='enroll_in_class'),
    
  
]
