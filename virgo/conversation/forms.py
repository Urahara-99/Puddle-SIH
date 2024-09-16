from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.template_pack = 'bootstrap5'
        self.helper.add_input(Submit('submit', 'Send'))
