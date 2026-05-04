from django import forms
from .models import CustomizationRequest

class CustomizationRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        template = kwargs.pop('template', None)
        super().__init__(*args, **kwargs)
        if template:
            self.fields['template'].initial = template
            self.fields['template'].widget = forms.HiddenInput()

    class Meta:
        model = CustomizationRequest
        fields = ['template', 'subject', 'description', 'budget_expectation']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'e.g., Add custom authentication layer'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500',
                'rows': 5,
                'placeholder': 'Tell us more about your requirements...'
            }),
            'budget_expectation': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Optional budget (USD)'
            }),
        }
