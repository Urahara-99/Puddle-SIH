from django.urls import path
from . import views

app_name = "item"

urlpatterns = [
    path("new/", views.new, name="new"),
    path("", views.items, name="items"),
    path('items/', views.items, name='items'),
    path("<int:pk>/edit/", views.edit_class, name="edit"),
    path("new/", views.new, name="new"),
    path("class_detail/<int:pk>/", views.class_detail, name="class_detail"),
    path("enroll/<int:course_id>/", views.enroll_in_class, name="enroll_in_class"),
    path('progress/', views.progress_page, name='progress_page'),
    path('progress/start/<int:class_id>/', views.start_progress, name='start_progress'),
    path('progress/finish/<int:class_id>/', views.finish_progress, name='finish_progress'),
    path("delete/<int:pk>/", views.delete_class, name="delete"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),
    path('domain/<int:domain_id>/', views.domain_detail, name='domain_detail'),
    path('enroll_domain/<int:domain_id>/', views.enroll_domain, name='enroll_domain'),
    path('inbox/<int:item_pk>/', views.inbox, name='inbox'),
]
