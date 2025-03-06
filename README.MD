# Plataforma de Aulas - Backend

Este é o backend da Plataforma de Aulas, desenvolvido em Django.

## 🚀 Como rodar o projeto localmente

### 1️⃣ Clone o repositório

```bash
  git clone https://github.com/iagoluancj/plataforma_aulas_backend.git
  cd plataforma_aulas_backend
  python -m venv venv
```

```bash
  source venv/bin/activate  # Mac/Linux
  venv\Scripts\activate  # Windows
```

```bash
pip install -r requirements.txt
```

```bash
SECRET_KEY = 'sua_chave_secreta'
NAME =  'nome_do_banco'
USER= 'usuario_do_banco'
PASSWORD= 'senha_do_banco'
HOST='localhost'
```

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#  Credenciais para teste após iniciar o servidor
**Estudante**
- Email: student@example.com
- Senha: student123

**Instrutor**
- Email: instructor@example.com
- Senha: instructor123

