from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CreateUserView, ClassViewSet, EnrollmentViewSet, LoginView, InstructorDashboardView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

schema_view = get_schema_view(
    openapi.Info(
        title="Plataforma Aulas API",
        default_version='v1',
        description="API para a plataforma de gestão de aulas online",
        contact=openapi.Contact(email="iagoluancj@gmail.com"),
        license=openapi.License(name="*** License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path("api/instructor/dashboard/scheduled_classes/", 
         InstructorDashboardView.as_view({"get": "scheduled_classes"}), 
    name="instructor-scheduled-classes"),
    path('api/register/', CreateUserView.as_view(), name='user-register'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)