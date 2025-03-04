from uuid import UUID
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import CustomUser, Classes, Enrollment
from .serializers import CustomUserSerializer, ClassesSerializer, EnrollmentSerializer
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
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer


# API de Inscrições
class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        queryset = Enrollment.objects.all()
        student_id = self.request.query_params.get('student')

        if student_id:
            queryset = queryset.filter(student_id=student_id)

        return queryset

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