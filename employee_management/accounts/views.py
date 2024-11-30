from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Form, FormField
from .forms import create_dynamic_form
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from django.db.models import Q
from .models import Employee, FormField
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import FormField
from .serializers import FormFieldSerializer


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user instance
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}! You have registered successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Authentication failed.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/change_password.html', {'form': form})



def form_builder(request):
    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        form = Form.objects.create(name=form_name)
        for key, value in request.POST.items():
            if key.startswith('field_'):
                label, field_type = value.split('|')
                FormField.objects.create(form=form, label=label, field_type=field_type)
        return redirect('view_form', form_id=form.id)

    return render(request, 'form_builder.html')

def view_form(request, form_id):
    form_obj = Form.objects.get(id=form_id)
    form_fields = form_obj.fields.all()
    DynamicForm = create_dynamic_form(form_fields)

    if request.method == 'POST':
        form = DynamicForm(request.POST)
        if form.is_valid():
            return render(request, 'form_success.html', {'form_data': form.cleaned_data})

    else:
        form = DynamicForm()

    return render(request, 'view_form.html', {'form': form, 'form_obj': form_obj})


def employee_create_update(request, employee_id=None):
    if request.method == 'GET':
        form = EmployeeForm(instance=Employee.objects.get(id=employee_id) if employee_id else None)
        return render(request, 'employee_form.html', {'form': form})

    elif request.method == 'POST':
        form = EmployeeForm(request.POST, instance=Employee.objects.get(id=employee_id) if employee_id else None)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Employee saved successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
        
        from django.shortcuts import render, get_object_or_404, redirect

def employee_list(request):
    search_query = request.GET.get('search', '')
    employees = Employee.objects.all()

    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    context = {
        'employees': employees,
        'search_query': search_query,
    }
    return render(request, 'employee_list.html', context)

def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return redirect('employee_list')



User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
      

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]




class DynamicFormFieldListView(generics.ListAPIView):
    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer





