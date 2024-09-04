from django.contrib import admin
from .models import Class, Domain, Resource, Skill, LearningPath, ExcelFile

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1

class ClassInline(admin.TabularInline):
    model = Class
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

class LearningPathInline(admin.TabularInline):
    model = LearningPath
    extra = 1

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    inlines = [SkillInline, ClassInline]  # Display Skills and Classes related to the Domain

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    inlines = [LearningPathInline]  # Display Learning Paths related to the Skill

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    inlines = [ResourceInline]  # Display Resources related to the Class

@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'uploaded_at')
    search_fields = ('title',)

