from rest_framework import serializers
from .models import CustomUser, Class, Enrollment
import uuid

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'role']
    
    def create(self, validated_data):
        validated_data['id'] = uuid.uuid4()  
        return super().create(validated_data)

class ClassSerializer(serializers.ModelSerializer):
    instructor = CustomUserSerializer(read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'title', 'description', 'scheduled_at', 'instructor']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

    def validate(self, data):
        if not data.get("student") or not data.get("class_obj"):
            raise serializers.ValidationError("Os campos student e class_obj são obrigatórios.")

        return data

    def validate_id(self, value):
        """Valida se o ID fornecido é um UUID válido."""
        try:
            return str(UUID(str(value)))
        except ValueError:
            raise serializers.ValidationError("ID inválido. Certifique-se de fornecer um UUID válido.")