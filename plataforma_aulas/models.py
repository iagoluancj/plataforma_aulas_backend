import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    profile_picture = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('student', 'Student')], default='student')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    class Meta:
        db_table = "custom_users"

class Class(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    scheduled_at = models.DateTimeField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="classes")

    class Meta:
        db_table = 'classes'

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="enrollments")
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'enrollments'
        unique_together = ('student', 'class_obj')  

    def __str__(self):
        return f"{self.student.username} -> {self.class_obj.title}"
