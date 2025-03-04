from rest_framework import serializers
from .models import CustomUser, Classes, Enrollment
import uuid

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'role']
    
    def create(self, validated_data):
        validated_data['id'] = uuid.uuid4()  
        return super().create(validated_data)

class ClassesSerializer(serializers.ModelSerializer):
    instructor_id = serializers.PrimaryKeyRelatedField(
        source="instructor", 
        queryset=CustomUser.objects.all()   
    )

    instructor_name = serializers.SerializerMethodField()

    class Meta:
        model = Classes
        fields = ['id', 'title', 'description', 'scheduled_at', 'instructor_id', 'instructor_name']

    def get_instructor_name(self, obj):
        return obj.instructor.full_name if hasattr(obj.instructor, 'full_name') else obj.instructor.username

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

    def validate(self, data):
        if not data.get("student") or not data.get("classes"):
            raise serializers.ValidationError("Os campos student e classes são obrigatórios.")

        return data