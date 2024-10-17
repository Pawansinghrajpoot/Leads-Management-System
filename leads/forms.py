from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'name', 'number', 'database', 
            'demo_lecture_attended', 'interested_in',
            'last_whatsapp_blast', 'response_to_whatsapp_blast', 
            'last_call_date', 'followup_of_last_call', 
            'close_reason'
        ]
        widgets = {
            'last_call_date': forms.DateInput(attrs={'type': 'date'}),
            'followup_of_last_call': forms.DateInput(attrs={'type': 'date'}),  # Follow-up date
        }

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class UserLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('This account is inactive.')
# leads/forms.py
from django import forms
from .models import Lead

class LeadCallDateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['last_call_date']
        widgets = {
            'last_call_date': forms.DateInput(attrs={'type': 'date'}),
        }
from django import forms
from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data
