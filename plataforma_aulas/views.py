from uuid import UUID
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import CustomUser, Classes, Enrollment
from .serializers import CustomUserSerializer, ClassWithEnrollmentsSerializer, UpdateUserSerializer, ClassesSerializer, EnrollmentSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .permissions import IsInstructor
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import action
from rest_framework import status

# API de Usuários
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    parser_classes = (MultiPartParser, FormParser)

    # Define o serializer de acordo com o metodo/ação da requisição.
    def get_serializer_class(self):
        if self.action in ['create']:  
            return CreateUserSerializer
        return UpdateUserSerializer  

    # Trata especificamente os arquivos que vem do profile_picture nos updates (put)
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            if 'profile_picture' in request.data:
                instance.profile_picture.delete(save=False)
            
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API para criação de usuário
class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({'message': 'User created successfully', 'user': serializer.data}, status=status.HTTP_201_CREATED)
            if 'email' in serializer.errors:
                return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API de Aulas
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer

    def get_queryset(self):
        try:
            instructor_id = self.request.query_params.get("instructor_id")
            return Classes.objects.filter(instructor_id=instructor_id) if instructor_id else Classes.objects.all()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Caso seja criação de classes, verifica se o usuário com o IsInstructor.
    def get_permissions(self):
        if self.action == 'create':  
            return [IsInstructor()]
        return [IsAuthenticated()]

    # Tratativa de erros
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API de Inscrições
class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        try:
            student_id = self.request.query_params.get('student')
            return Enrollment.objects.filter(student_id=student_id) if student_id else Enrollment.objects.all()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("senha")  
            user = authenticate(request, email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token 
                access_token["role"] = getattr(user, "role", 0)
                return Response({
                    "access": str(access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "full_name": user.full_name,
                        "email": user.email,
                        "role": user.role,
                        "profile_picture": user.profile_picture.url if user.profile_picture else None,
                    }
                })
            return Response({"error": "Credenciais inválidas"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InstructorDashboardView(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def scheduled_classes(self, request):
        try:
            instructor = request.user
            classes = Classes.objects.filter(instructor=instructor)
            serializer = ClassWithEnrollmentsSerializer(classes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)