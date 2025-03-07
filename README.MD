# Plataforma de Aulas - Backend
**Descrição**: Este projeto é uma plataforma de gestão de aulas online, desenvolvida com Django e Django REST Framework, utilizando SQL Server como banco de dados. Ele permite o gerenciamento completo de aulas, participantes e perfis de usuários, seguindo uma arquitetura segura e escalável.

O sistema oferece operações CRUD para aulas, incluindo campos como título, descrição, data, hora e instrutor. Além disso, implementa o registro de participação de alunos, possibilitando a inscrição em aulas disponíveis. Conta com autenticação e autorização via tokens JWT, garantindo permissões distintas para alunos e instrutores.

> ### [Documentação do Front-end](https://github.com/iagoluancj/plataforma_aulas_frontend)

## Pré Requisitos:
- Python (>= 3.8)
- Django (>= 3.2)
- Banco de Dados: Microsoft SQL Server, pode ser instalado a partir desse [link](https://www.microsoft.com/en-us/sql-server/sql-server-downloads).
- Driver ODBC para SQL Server (necessário para a conexão com o banco de dados MSSQL): <br>
Windows: Pode ser instalado a partir do [link oficial da Microsoft](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16). <br>
Linux: Instale o driver usando o seguinte comando (para distribuições baseadas em Debian, como Ubuntu):

## Funcionalidades:
- **Gerenciamento de Cursos:** Permite que instrutores realizem operações CRUD (criação, leitura, atualização e exclusão) de aulas, incluindo informações detalhadas como título, descrição, data, hora, instrutor e o vídeo da aula.
- **Gerenciamento de Usuários:** Controle de usuários (estudantes e instrutores) com autenticação via JWT, cadastro de novos usuários e diferenciação de permissões por tipo de perfil.
- **Agendamento de Aulas:** Estudantes podem se inscrever (enrollments) nas aulas disponíveis ministradas pelos instrutores.
- **Fornecimento de Dados para o Dashboard:** Endpoint que retorna informações filtradas e indexadas para a construção do painel de controle no frontend.

## Funcionalidades Extras
- **Cadastro de usuário:** Permite a criação de novos usuários diretamente pelo frontend, garantindo maior autonomia e flexibilidade na gestão de acessos.
- **Consistência e Segurança dos Dados:** Implementação de tratamento de erros (try/except) e propagação de exclusões para garantir integridade nos relacionamentos entre dados.

## Instalação:
### Clone o Repositório:
```
git clone https://github.com/iagoluancj/plataforma_aulas_backend.git
cd plataforma_aulas_backend
```

### Crie e ative o Ambiente Virtual:
```
-Linux:
python3 -m venv venv
source venv/bin/activate

-Windows:
python -m venv venv
```

```
venv\Scripts\activate
```

### Baixe as Dependências do Projeto:
```
pip install requirements.txt
```

### Configurar Variáveis de Ambiente: 
Crie um arquivo .env baseado no exemplo abaixo para configuração do banco de dados e outras varíaveis importantes:
```
SECRET_KEY = 'sua_chave_secreta'
NAME =  'nome_do_banco'
USER= 'usuario_do_banco'
PASSWORD= 'senha_do_banco'
HOST='localhost'
```

- Para obtenção de uma nova SECRET_KEY:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Aplique as Migrações no seu banco:
```
python manage.py makemigrations
python manage.py migrate
```

## Uso:
1. Para inicializar a aplicação:
```
python manage.py runserver
```
2. Caso o front-end já esteja configurado, basta acessar [Local host](http://localhost:3000/). 
2.1 Caso ainda não esteja, acesse: [Documentação frontend](https://github.com/iagoluancj/plataforma_aulas_frontend)

3. Acesso pode ser realizado no navegador através do http://127.0.0.1:8000/ - Para mais informações End-Points acesse a documentação no último tópico.

4. Para acesso aos End-Points é necessário um Token JWT , com o usuário criado em sistema com o JWT faça uma requisição **POST** em
http://127.0.0.1:8000/api/auth/login/ com o corpo da requisição no formato:
```
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```
- Isso retornará um Token JWT necessário para demais requisições da API na seguinte forma:
 ```
{
  "refresh": "refresh_token",
  "access": "acess_token"
}
 ```
> *Obs: Há diferenciação nos acessos conforme a role do usuário. Apenas usuários com a role "admin" (instrutores) podem realizar requisições POST em /classes/, enquanto usuários com a role "student" têm permissão apenas para GET. Além disso, todas as rotas exigem autenticação, não permitindo acessos de anonymous users. Portanto, é necessário incluir o token de autenticação em todas as requisições, exceto na rota de login.*

## Documentação:
Toda a aplicação se encontra documentada através do Swagger, a mesma pode ser visualizada da seguinte forma:
1. Inicie a aplicação com
```
python manage.py runserver
```
2. Acesse o seguinte end_point:
```
http://127.0.0.1:8000/swagger
```
