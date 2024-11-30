from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, LogoutView
from .views import DynamicFormFieldListView


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('employee/create/', views.employee_create_update, name='employee_create'),
    path('employee/update/<int:employee_id>/', views.employee_create_update, name='employee_update'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/formfields/', DynamicFormFieldListView.as_view(), name='form_field_list'),
]

from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet

router = DefaultRouter()
router.register(r'api/employees', EmployeeViewSet)

urlpatterns += router.urls

