from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Classes, Enrollment
import uuid

# Serializer para criar novos usuários
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'password', 'role', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}  
    
    def create(self, validated_data):
        validated_data['id'] = uuid.uuid4()
        password = validated_data.pop('password')  
        user = CustomUser(**validated_data)
        user.set_password(password)  
        user.save()
        return user

# Serializer para permitir update sem ter a senha como obrigatória
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'role', 'profile_picture'] 

# Serializer para criar novas classes
class ClassesSerializer(serializers.ModelSerializer):

    # somente users da role instructor podem acessar esse serializer.
    instructor_id = serializers.PrimaryKeyRelatedField(
        source="instructor", 
        queryset=CustomUser.objects.all()   
    )

    instructor_name = serializers.SerializerMethodField()

    class Meta:
        model = Classes
        fields = ['id', 'title', 'description', 'scheduled_at', 'instructor_id', 'instructor_name', 'link_video']

    def get_instructor_name(self, obj):
        return obj.instructor.full_name if hasattr(obj.instructor, 'full_name') else obj.instructor.username

# Serializer a parte para criar uma view dos dados já filtrados pro frontned.
class ClassWithEnrollmentsSerializer(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Classes
        fields = ['id', 'title', 'scheduled_at', 'participants_count']

    def get_participants_count(self, obj):
        return obj.classes_enrollments.count()  

# Serializer para realizar as inscrições de classes x students
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

    def validate(self, data):
        if not data.get("student") or not data.get("classes"):
            raise serializers.ValidationError("Os campos student e classes são obrigatórios.")

        return data

# Serializer para criar o token de acesso
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token
