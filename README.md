# 🗓️ Sistema de Agendamento de Salas

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.2.6-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue?logo=postgresql)
![License](https://img.shields.io/badge/license-MIT-yellow)
![Status](https://img.shields.io/badge/status-Em%20Desenvolvimento-orange)

---

## 📖 Introdução

O **Sistema de Agendamento de Salas** é uma aplicação web desenvolvida com o **framework Django** e o banco de dados **PostgreSQL**, criada para gerenciar o uso de salas corporativas ou institucionais.

O sistema permite:
- ✅ Cadastrar usuários e definir seus cargos e permissões.  
- 🏢 Cadastrar salas com controle de disponibilidade.  
- 📅 Realizar agendamentos com verificação automática de conflitos de horário.  
- 🔐 Acessar um painel administrativo completo via Django Admin.  

Esse projeto foi desenvolvido seguindo boas práticas de **arquitetura MVC**, **componentização de templates** e **separação de camadas lógicas** (model, view, template e static).

---

## ⚙️ Tecnologias Utilizadas

| Categoria | Tecnologia |
|------------|-------------|
| **Linguagem** | Python 3.12+ |
| **Framework Web** | Django 5.2.6 |
| **Banco de Dados** | PostgreSQL |
| **Frontend** | HTML5, CSS (Tailwind), JavaScript |
| **Ambiente Virtual** | Virtualenv |
| **IDE** | VS Code |
| **Controle de Versão** | Git + GitHub |

---

## 🧩 Modelo Conceitual (DER)

O modelo a seguir representa o relacionamento entre as principais entidades do sistema:  
**Usuário**, **Sala**, **Agendamento** e **AgendamentoUsuario**.

![Modelo Conceitual](https://github.com/user-attachments/assets/9ba47cab-4d3f-4563-8999-3500afa5a14e)

---

## 🗂️ Estrutura de Pastas do Projeto

```bash
Sistema-de-Agendamento/
│
├── agendamento/                     # Aplicação principal do sistema
│   ├── migrations/                  # Histórico de migrações do banco
│   ├── admin.py                     # Registro de modelos no painel admin
│   ├── apps.py                      # Configuração da aplicação
│   ├── criar_sala.py                # View para criação de salas
│   ├── criar_usuario.py             # View para criação de usuários
│   ├── form_agendamento.py          # Formulário de agendamento
│   ├── form_registro.py             # Formulário de registro de usuário
│   ├── form_usuario.py              # Formulário de edição de usuário
│   ├── models.py                    # Modelos de dados e regras de negócio
│   ├── tests.py                     # Testes automatizados
│   ├── views.py                     # Controladores e regras de visualização
│
├── SistemaAgendamento/              # Configurações do projeto Django
│   ├── settings.py                  # Configurações gerais e banco de dados
│   ├── urls.py                      # Rotas do sistema
│   ├── wsgi.py / asgi.py
│
├── static/                          # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   │   └── output.css
│   ├── images/
│   │   ├── add.svg, busca.svg, edit.svg, delete.svg, logout.svg, etc.
│   │   └── fundoTelas.png
│   ├── js/
│   │   ├── agendamento.js
│   │   ├── modal_agendamento.js
│   │   ├── modal_editar.js
│   │   ├── nova_sala.js
│   │   ├── novo_usuario.js
│   │   └── perfil.js
│
├── templates/                       # Templates HTML do sistema
│   ├── admin/
│   │   └── usuarios_admin.html
│   ├── partials/
│   │   └── _form_agendamento.html
│   ├── registration/
│   │   ├── agendamentos_usuario.html
│   │   ├── base.html / base_interna.html
│   │   ├── index.html
│   │   ├── perfil.html
│   │   └── modal_agendamento.html
│
├── manage.py                        # Comando administrativo do Django
├── package.json / package-lock.json  # Dependências JS
├── venv/                            # Ambiente virtual
└── README.md
```

# 🧱 Modelos Django

### 🧍‍♂️ `Usuario`

Extende `AbstractUser`, utilizando **e-mail como identificador principal** e permitindo diferentes cargos e tipos de usuário.

**Campos principais:**
- `email` (login principal)  
- `tipo_usuario`: `Admin` | `Comum`  
- `cargo`: `Diretor`, `Gerente`, `Funcionário`, etc.

---

### 🏢 `Sala`

Contém as informações das salas cadastradas, incluindo nome, capacidade e criador.

**Campos:**
- `nome`  
- `capacidade`  
- `localizacao`  
- `criador` (usuário responsável)

---

### 📅 `Agendamento`

Representa as reservas de salas e contém validações automáticas.

**Campos:**
- `nome`  
- `sala`  
- `data`  
- `hora_inicio`  
- `hora_fim`  
- `criador`  
- `codigo_agendamento` (gerado automaticamente)

**Validações:**
1. Não permite agendar no passado.  
2. Exige `hora_fim` > `hora_inicio`.  
3. Impede conflito de horários na mesma sala.

---

### 👥 `AgendamentoUsuario`

Tabela intermediária para relacionamento *muitos-para-muitos* entre usuários e agendamentos.

---

# 🧠 Regras de Negócio

As principais regras são implementadas no método `clean()` do modelo `Agendamento`:

- **Conflito de horário:**  
  Impede sobreposição de horários na mesma sala.  

- **Data inválida:**  
  Bloqueia agendamentos no passado.  

- **Hora final menor:**  
  Impede que `hora_fim` seja menor ou igual a `hora_inicio`.  

Além disso, o sistema gera automaticamente um `codigo_agendamento` único.

---

# 🔐 Painel Administrativo

O **Django Admin** oferece gerenciamento completo de:

- Usuários (`UsuarioAdmin`)  
- Salas (`SalaAdmin`)  
- Agendamentos (`AgendamentoAdmin`)  
- Participações (`AgendamentoUsuarioAdmin`)

---

# 🗃️ Configuração do Banco de Dados

Configuração padrão em `settings.py`:

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
pip install django-widget-tweaks
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

## 🧩 Estrutura do Frontend

### 🎨 **CSS**

Local: `static/css/output.css`  
Baseado em **TailwindCSS**, com customizações manuais para identidade visual limpa e moderna.

---

### 🖼️ **Imagens**

Local: `static/images/`  
Contém ícones SVG, imagens de fundo e botões de ação.

---

### ⚙️ **JavaScript**

Scripts responsáveis pela interatividade da interface:

- `agendamento.js`: Carrega e atualiza agendamentos.  
- `modal_agendamento.js`: Controle do modal de criação.  
- `modal_editar.js`: Edição dinâmica de agendamentos.  
- `nova_sala.js`: Criação de novas salas.  
- `novo_usuario.js`: Registro de usuários.  
- `perfil.js`: Exibição e edição de perfil.  

---

### 🧱 **Templates**

Páginas HTML do sistema, com herança e componentes reutilizáveis:

- `base.html` — layout principal  
- `index.html` — tela inicial  
- `perfil.html` — dados do usuário  
- `agendamentos_usuario.html` — listagem de reservas  
- `_form_agendamento.html` — formulário parcial reutilizado  

---

## 🔍 Funcionalidades Principais

| Funcionalidade | Descrição |
|----------------|------------|
| **Cadastro de Usuário** | Permite registro e definição de tipo (Admin/Comum). |
| **Login e Autenticação** | Autenticação via e-mail e senha. |
| **Cadastro de Sala** | Adiciona novas salas e define capacidade/localização. |
| **Agendamento de Sala** | Cria reservas com validação de conflito. |
| **Edição e Cancelamento** | Permite editar e remover agendamentos existentes. |
| **Painel Admin** | Gerenciamento completo de dados. |

---
