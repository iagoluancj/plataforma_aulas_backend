from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ClassViewSet, EnrollmentViewSet, LoginView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/login/', LoginView.as_view(), name='login'),
]