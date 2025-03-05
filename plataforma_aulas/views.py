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
    # permission_classes = [IsAuthenticated]
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
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if 'profile_picture' in request.data:
            instance.profile_picture.delete(save=False)  

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

# API para criação de usuário
class CreateUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        # Tratativa de erros
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully', 'user': serializer.data, 'status': status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        
        # Tratativa de erros
        if 'email' in serializer.errors:
            return Response(
                {'error': 'Email is already in use. Please choose another one.', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API de Aulas
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer

    # Caso seja criação de classes, verifica se o usuário com o IsInstructor.
    def get_permissions(self):
        if self.action == 'create':  
            return [IsInstructor()]
        return [IsAuthenticated()]

    # Tratativa de erros
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": serializer.errors, "status": status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# API de Inscrições
class EnrollmentViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        queryset = Enrollment.objects.all()
        student_id = self.request.query_params.get('student')

        if student_id:
            queryset = queryset.filter(student_id=student_id)

        return queryset

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    # permission_classes = [AllowAny]


    # @ratelimit(key='ip', rate='5/m', method='POST', block=True)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("senha")  

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "role": user.role,
                    "profile_picture": user.profile_picture.url if user.profile_picture else None

                }
            })
        else:
            return Response({"error": "Credenciais inválidas"}, status=400)

class InstructorDashboardView(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]  

    @action(detail=False, methods=['get'])
    def scheduled_classes(self, request):
        # Filtra as aulas com base no instrutor da requisição
        instructor = request.user
        classes = Classes.objects.filter(instructor=instructor)

        # Busca aulas com a contagem de participantes
        serializer = ClassWithEnrollmentsSerializer(classes, many=True)
        return Response(serializer.data)