from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CreateUserView, ClassViewSet, EnrollmentViewSet, LoginView, InstructorDashboardView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path("api/instructor/dashboard/scheduled_classes/", 
         InstructorDashboardView.as_view({"get": "scheduled_classes"}), 
    name="instructor-scheduled-classes"),
    path('api/register/', CreateUserView.as_view(), name='user-register'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)