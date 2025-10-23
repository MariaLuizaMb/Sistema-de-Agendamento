# 🗓️ Sistema de Agendamento de Salas

## 📖 Introdução

O **Sistema de Agendamento de Salas** foi desenvolvido com o objetivo de gerenciar o uso de salas corporativas, permitindo o **cadastro de usuários, salas e agendamentos**, além de realizar o controle de disponibilidade e evitar conflitos de horários.  
O projeto foi construído utilizando o **framework Django (Python)** e o banco de dados **PostgreSQL**, garantindo segurança, organização e escalabilidade.

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.12+**
- **Django 5.2.6**
- **PostgreSQL**
- **Virtualenv**
- **VS Code**

---

## 🧩 Modelo Conceitual (DER)

O diagrama abaixo representa a estrutura lógica do banco de dados do sistema, destacando as entidades principais e seus relacionamentos:

<img width="1748" height="1264" alt="Diagrama ER de banco de dados (pé de galinha)" src="https://github.com/user-attachments/assets/9ba47cab-4d3f-4563-8999-3500afa5a14e" />


### Descrição das Entidades

#### 🧑‍💼 Usuário
- **ID**: Identificador único.  
- **username**: Nome de usuário.  
- **email**: E-mail único (utilizado como login).  
- **tipo_usuario**: Define se o usuário é *Admin* ou *Comum*.  
- **cargo**: Cargo ocupado (Diretor, Gerente, Coordenador ou Funcionário).

#### 🏢 Sala
- **nome**: Identificador único da sala.  
- **capacidade**: Número máximo de pessoas.  
- **tipo_sala**: Categoria da sala (reunião, trabalho, brainstorming etc.).  
- **criador**: Referência ao usuário que cadastrou a sala.

#### 📅 Agendamento
- **sala**: Sala reservada.  
- **criador**: Usuário que criou o agendamento.  
- **nome**: Nome da reunião.  
- **data**: Data da reserva.  
- **hora_inicio / hora_fim**: Intervalo de tempo reservado.  
- **status**: Estado do agendamento (ativo ou cancelado).  
- **codigo_agendamento**: Código único gerado automaticamente.

#### 👥 AgendamentoUsuario
- **agendamento**: Referência a um agendamento.  
- **usuario**: Participante vinculado ao agendamento.  
- Essa tabela implementa a relação *muitos-para-muitos* entre **Agendamento** e **Usuário**.

---

## 🗂️ Estrutura de Pastas do Projeto

A seguir, a estrutura completa do projeto Django, representada em formato de árvore:

```
Sistema-de-Agendamento/
│
├── agendamento/                     # Aplicação principal do sistema
│   ├── __pycache__/                 # Arquivos compilados
│   ├── migrations/                  # Controle de versões do banco de dados
│   │   ├── __init__.py
│   ├── admin.py                     # Configuração do painel administrativo
│   ├── apps.py                      # Registro da aplicação
│   ├── models.py                    # Modelos de dados e regras de negócio
│   ├── tests.py                     # Testes automatizados
│   ├── views.py                     # Lógica das views e controladores
│
├── SistemaAgendamento/              # Diretório de configuração principal
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                  # Configurações globais do projeto
│   ├── urls.py                      # Rotas e URLs do sistema
│   ├── wsgi.py                      # Interface com o servidor web
│            
│
├── venv/                            # Ambiente virtual do projeto
│
├── manage.py                        # Script de administração do Djan
├── .gitignore                       # Arquivos ignorados pelo Git
└── README.md                        # Documentação do projeto
```

---

## 🧱 Modelos Django

### 🔹 `Usuario`
Extende a classe `AbstractUser`, permitindo autenticação personalizada por e-mail e diferenciação entre perfis administrativos e comuns.  
Inclui os campos `tipo_usuario` e `cargo` para controle hierárquico de permissões.

### 🔹 `Sala`
Define os atributos principais das salas e inclui o campo `criador` para identificar o responsável pelo cadastro.  
O relacionamento com `Usuario` utiliza `on_delete=models.SET_NULL`, garantindo que a sala não seja excluída se o criador for removido.

### 🔹 `Agendamento`
Representa as reservas das salas.  
Inclui validações automáticas para:
- Impedir agendamentos no passado.  
- Verificar se `hora_fim` é posterior a `hora_inicio`.  
- Evitar sobreposição de horários na mesma sala.  

Além disso, o campo `codigo_agendamento` é gerado automaticamente com base no ID do criador e do agendamento.

### 🔹 `AgendamentoUsuario`
Tabela intermediária para o relacionamento *muitos-para-muitos* entre usuários e agendamentos.  
Cada usuário pode participar de várias reuniões e cada agendamento pode conter vários participantes.

---

## 🧠 Regras de Negócio e Validações

As validações são implementadas no método `clean()` da classe `Agendamento`:

1. **Validação de horário:**  
   Impede que o horário final seja anterior ou igual ao horário inicial.  
2. **Validação de data:**  
   Bloqueia o agendamento de reuniões no passado.  
3. **Validação de conflito:**  
   Verifica se já existe outro agendamento ativo para a mesma sala e horário.

Essas verificações garantem a consistência e a integridade dos dados no sistema.

---

## 🔐 Painel Administrativo

O arquivo `admin.py` registra as classes no **Django Admin**, permitindo:
- Visualizar, criar, editar e excluir usuários, salas e agendamentos.  

As classes registradas:
- `UsuarioAdmin`
- `SalaAdmin`
- `AgendamentoAdmin`
- `AgendamentoUsuarioAdmin`

---

## 🗃️ Configuração do Banco de Dados

O sistema utiliza o **PostgreSQL** como SGBD principal, configurado em `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'agendamento_salas',
        'USER': 'postgres',
        'PASSWORD': '1289',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

O modelo de usuário é redefinido para utilizar o campo `email` como identificador principal:

```python
AUTH_USER_MODEL = 'agendamento.Usuario'
```

---

## 🚀 Execução do Projeto

### 1️⃣ Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 2️⃣ Instalar dependências
```bash
pip install django psycopg2-binary
```

### 3️⃣ Criar e aplicar migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ Criar superusuário
```bash
python manage.py createsuperuser
```

### 5️⃣ Executar o servidor
```bash
python manage.py runserver
```

O sistema estará disponível em:  
📍 **http://127.0.0.1:8000/**

---
