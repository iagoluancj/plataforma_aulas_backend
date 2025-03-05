import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Model que utiliza do user já presente pelo django
class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)

# Model para criar usuário customizado
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('student', 'Student')], default='student')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  #
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager() 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

    class Meta:
        db_table = "custom_users"

# Model para criar as classes
class Classes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    scheduled_at = models.DateTimeField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="taught_classes")

    class Meta:
        db_table = 'classes'

    def __str__(self):
        return self.title

# Model para criar as associações de classes x users
class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="student_enrollments")
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name="classes_enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'enrollments'
        constraints = [
            models.UniqueConstraint(fields=['student', 'classes'], name='unique_student_class_enrollment')
    ] 

    def __str__(self):
        return f"{self.student.full_name} -> {self.classes.title}"
