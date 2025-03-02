from uuid import UUID
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import CustomUser, Class, Enrollment
from .serializers import CustomUserSerializer, ClassSerializer, EnrollmentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# API de Usuários
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        print("Request Data:", request.data)  
        return super().create(request, *args, **kwargs)

# API de Aulas
class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def perform_create(self, serializer):
        default_instructor_id = UUID("9AC16DAA-7861-4FB4-9872-5462B9A1FAEE")

        try:
            default_instructor = CustomUser.objects.get(id=default_instructor_id)  
        except ObjectDoesNotExist:
            raise ValueError(f"O usuário instrutor padrão com ID {default_instructor_id} não existe no banco de dados.")

        instructor = self.request.user if self.request.user.is_authenticated else default_instructor
        serializer.save(instructor=instructor)

# API de Inscrições
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("senha")  

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        else:
            return Response({"error": "Credenciais inválidas"}, status=400)