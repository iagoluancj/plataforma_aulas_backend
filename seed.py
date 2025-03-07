import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plataforma_aulas.settings')
django.setup()

from django.utils.timezone import now
from datetime import timedelta
from plataforma_aulas.models import CustomUser, Classes, Enrollment
from datetime import datetime, timedelta

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
    print(f"Instrutor encontrado: {instructor.email}")

    if instructor:
        aulas = [
            ("Introdução ao Django", "Conceitos iniciais de Django e Django Rest Framework"),
            ("APIs Restful", "Como construir APIs RESTful com Django Rest Framework"),
            ("React Avançado", "Técnicas e padrões para aplicações complexas em React: Aprofunde-se em hooks, otimização e gerenciamento de estados em React"),
            ("TypeScript", "Aprenda com TypeScript como adicionar tipagem estática para criar códigos mais seguros e fáceis de manter"),
            ("SQL Server", "Aprenda a melhorar o desempenho e a criação de consultas eficientes no SQL Server")
        ]

        created_classes = []

        for i, (title, description) in enumerate(aulas, start=2):
            try:
                meses = random.randint(0, 11) 
                data_matricula = datetime.now() - timedelta(days=meses * 30)

                class1 = Classes.objects.create(
                    title=title,
                    description=description,
                    scheduled_at=data_matricula,
                    instructor=instructor,
                )
                created_classes.append(class1)
                print(f"Classe '{class1.title}' criada com sucesso.")
            except Exception as e:
                print(f"Erro ao criar a classe {title}: {e}")

        alunos = []
        for i in range(5):
            aluno = CustomUser.objects.create_user(
                email=f"student{i+1}@example.com",
                full_name=f"Aluno Teste {i+1}",
                password=f"student{100+i+1}",
                role="student"
            )
            alunos.append(aluno)
            print(f"Aluno {aluno.full_name} criado com sucesso.")

        for i, aluno in enumerate(alunos):
            aulas_para_aluno = random.sample(created_classes, random.randint(1, 3))  
            for aula in aulas_para_aluno:
                try:
                    Enrollment.objects.create(student=aluno, classes=aula)
                    print(f"Aluno {aluno.full_name} matriculado na aula '{aula.title}'.")
                except Exception as e:
                    print(f"Erro ao matricular aluno {aluno.full_name} na aula {aula.title}: {e}")

if __name__ == "__main__":
    seed_database()
