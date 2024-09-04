from django import forms
from .models import Class, Resource, ExcelFile, Domain, LearningPath

INPUT_CLASSES = "w-full py-4 px-6 rounded-xl bg-gray-100 text-gray-700 border-gray-300"

# Form for creating new domains
class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = ('name', 'images')
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'images': forms.ClearableFileInput(attrs={'class': INPUT_CLASSES}),
        }

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = (
            "domain",
            "class_name",
            "learning_paths",  # Add learning_paths field
            "description",
            # Remove the lines below if these fields no longer exist in the model
             "pdf",
             "video",
             "document",
        )
        widgets = {
            "domain": forms.Select(attrs={"class": INPUT_CLASSES}),
            "class_name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "learning_paths": forms.CheckboxSelectMultiple(attrs={"class": INPUT_CLASSES}),  # Use checkbox for multiple selections
            "description": forms.Textarea(attrs={"class": INPUT_CLASSES}),
            # Comment or remove these lines if those fields no longer exist
             "pdf": forms.FileInput(attrs={"class": INPUT_CLASSES}),
             "video": forms.FileInput(attrs={"class": INPUT_CLASSES}),
             "document": forms.FileInput(attrs={"class": INPUT_CLASSES}),
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('resource_type', 'file')
        widgets = {
            'resource_type': forms.Select(attrs={'class': INPUT_CLASSES}),
            'file': forms.ClearableFileInput(attrs={'class': INPUT_CLASSES}),
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = (
            "domain",
            "class_name",
            "learning_paths",  # Add learning_paths field
            "description",
        )
        widgets = {
            "domain": forms.Select(attrs={"class": INPUT_CLASSES}),
            "class_name": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "learning_paths": forms.CheckboxSelectMultiple(attrs={"class": INPUT_CLASSES}),  # Use checkbox for multiple selections
            "description": forms.Textarea(attrs={"class": INPUT_CLASSES}),
        }

class ExcelUploadForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'file': forms.ClearableFileInput(attrs={'class': INPUT_CLASSES}),
        }

class LearningPathForm(forms.ModelForm):
    resources = forms.ModelMultipleChoiceField(
        queryset=Resource.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = LearningPath
        fields = ['name', 'description', 'resources']