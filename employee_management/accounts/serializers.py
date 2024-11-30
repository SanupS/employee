from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Employee
from rest_framework import serializers
from .models import FormField


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
   
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

       

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = '__all__'


