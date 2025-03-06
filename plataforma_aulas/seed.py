import os
import django
from django.utils.timezone import now
from datetime import timedelta
from plataforma_aulas.models import CustomUser, Classes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')
django.setup()

def seed_database():
    if not CustomUser.objects.filter(email="student@example.com").exists():
        student = CustomUser.objects.create_user(
            email="student@example.com",
            full_name="Estudante Teste",
            password="student123",
            role="student"
        )
        print(f"Usuário {student.email} criado com sucesso.")

    if not CustomUser.objects.filter(email="instructor@example.com").exists():
        instructor = CustomUser.objects.create_user(
            email="instructor@example.com",
            full_name="Instrutor Teste",
            password="instructor123",
            role="admin"
        )
        print(f"Usuário {instructor.email} criado com sucesso.")

    instructor = CustomUser.objects.filter(role="admin").first()
    if instructor and not Classes.objects.exists():
        class1 = Classes.objects.create(
            title="Aula de Django",
            description="Introdução ao Django Rest Framework",
            scheduled_at=now() + timedelta(days=2),
            instructor=instructor,
            link_video="https://www.youtube.com/watch?v=exemplo"
        )
        print(f"Classe '{class1.title}' criada com sucesso.")

if __name__ == "__main__":
    seed_database()
