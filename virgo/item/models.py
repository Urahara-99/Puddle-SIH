from django.db import models
from django.contrib.auth.models import User

class Domain(models.Model):
    name = models.CharField(max_length=225, unique=True)
    images = models.ImageField(upload_to='domain_images/', blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Domains"

    def __str__(self):
        return self.name

    def get_classes(self):
        return self.classes.all()

    def get_total_classes(self):
        return self.classes.count()

    def get_completed_classes(self, user):
        completed_classes = Enrollment.objects.filter(user=user, course__domain=self).count()
        return completed_classes

    def get_progress_percentage(self, user):
        total_classes = self.classes.count()
        completed_classes = self.classes.filter(enrollment__user=user, enrollment__is_completed=True).count()

        if total_classes > 0:
            return (completed_classes / total_classes) * 100
        return 0

class Skill(models.Model):
    domain = models.ForeignKey(Domain, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class LearningPath(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='learning_paths')
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Class(models.Model):
    domain = models.ForeignKey(Domain, related_name='classes', on_delete=models.CASCADE)
    class_name = models.CharField(max_length=255)
    description = models.TextField()
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    learning_paths = models.ManyToManyField(LearningPath, blank=True, related_name='classes')
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.class_name
    
    def get_classes(self):
        return self.classes.all()

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('image', 'Image'),
        ('excel', 'Excel File'),
    ]

    name = models.CharField(max_length=255)
    class_instance = models.ForeignKey(Class, related_name='resources', on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='resources/')

    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"

class ExcelFile(models.Model):
    domain = models.ForeignKey(Domain, related_name='excel_files', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='excel_files/')
    image = models.ImageField(upload_to='excel_images/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('finished', 'Finished'),
        ('ended', 'Ended'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')

    def __str__(self):
        return f"{self.user} - {self.course} - {self.status}"

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.class_name}"

    def get_time_spent(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
