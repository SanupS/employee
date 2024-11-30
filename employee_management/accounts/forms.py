from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Employee, FormField  # Consolidate imports


# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Use CustomUser instead of the default User
        fields = ('username', 'email', 'password1', 'password2')


# Dynamic Form Creation Function
def create_dynamic_form(form_fields):
    class DynamicForm(forms.Form):
        pass

    # Dynamically add fields to DynamicForm using setattr
    for field in form_fields:
        if field.field_type == 'text':
            setattr(DynamicForm, field.label, forms.CharField(label=field.label))
        elif field.field_type == 'number':
            setattr(DynamicForm, field.label, forms.IntegerField(label=field.label))
        elif field.field_type == 'date':
            setattr(DynamicForm, field.label, forms.DateField(
                label=field.label,
                widget=forms.DateInput(attrs={'type': 'date'})
            ))
        elif field.field_type == 'password':
            setattr(DynamicForm, field.label, forms.CharField(
                label=field.label,
                widget=forms.PasswordInput
            ))

    return DynamicForm


# Employee Form
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email']
