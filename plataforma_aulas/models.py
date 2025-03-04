import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('student', 'Student')], default='student')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    class Meta:
        db_table = "custom_users"

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
