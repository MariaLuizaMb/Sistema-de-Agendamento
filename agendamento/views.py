from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.db.models import Q
from .models import Agendamento, Usuario
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .form_agendamento import AgendamentoForm
from .form_registro import RegisterForm
from .form_usuario import UsuarioForm, CustomPasswordChangeForm

class CustomLoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        """Exibe a página de login."""
        return render(request, self.template_name)

    def post(self, request):
        """Processa o envio do formulário de login."""
        email = request.POST.get('email')
        password = request.POST.get('password')

         # Verifica se o email existe no banco
        try:
            user_obj = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, "Este email não está registrado.")
            return render(request, self.template_name)

        # Verifica se o usuário está ativo
        if not user_obj.is_active:
            messages.error(request, "Esta conta está desativada. Contate o administrador.")
            return render(request, self.template_name)

        # Tenta autenticar com email e senha
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, "Senha incorreta. Tente novamente.")
            return render(request, self.template_name)

        # Tudo certo → faz login e redireciona
        login(request, user)
        return redirect('home')
    
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso. Faça login.")
            return redirect('login')
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect('login')

@login_required
def home(request):
    form = AgendamentoForm()
    """Página principal com listagem, filtro e pesquisa de agendamentos."""

    ordenar_por = request.GET.get('ordenar_por', '')
    termo_busca = request.GET.get('busca', '').strip()

    opcoes_validas = {
        'data': 'data',
        'hora_inicio': 'hora_inicio',
        'hora_fim': 'hora_fim',
        'sala': 'sala__nome',
        'criador': 'criador__username',
        'nome': 'nome',
        'codigo_agendamento': 'codigo_agendamento',
    }

    campo_ordenacao = opcoes_validas.get(ordenar_por, 'data')  # padrão: data

    agendamentos = Agendamento.objects.all()

    if termo_busca:
        agendamentos = agendamentos.filter(
            Q(nome__icontains=termo_busca) |
            Q(criador__username__icontains=termo_busca) |
            Q(sala__nome__icontains=termo_busca) |
            Q(status__icontains=termo_busca) |
            Q(data__icontains=termo_busca)
        )

    agendamentos = agendamentos.order_by(campo_ordenacao)

    if is_admin(request.user):
        template_name = 'admin/index_adm.html'
    else:
        template_name = 'index.html'


    return render(request, template_name, {
        'agendamentos': agendamentos,
        'form': form,
        'ordenar_por': ordenar_por,
        'busca': termo_busca,
    })
    
@login_required
def listar_usuarios(request):
    busca = request.GET.get('busca', '')
    ordenar_por = request.GET.get('ordenar_por', '')  # padrão: ordenar por ID

    usuarios = Usuario.objects.all()

    # Filtro de busca
    if busca:
        usuarios = usuarios.filter(username__icontains=busca)

    opcoes_validas = {
        'id': 'id',
        'nome': 'username',
        'tipo': 'tipo_usuario',
        'cargo': 'cargo',
    }

    campo_ordenacao = opcoes_validas.get(ordenar_por, 'id')  # padrão: ID
    usuarios = usuarios.order_by(campo_ordenacao)

    context = {
        'usuarios': usuarios,
        'busca': busca,
        'ordenar_por': ordenar_por,
    }

    return render(request, 'admin/usuarios_admin.html', context)

@login_required
def usuario_agendamentos(request):
    form = AgendamentoForm()
    """Página principal com listagem, filtro e pesquisa de agendamentos."""

    ordenar_por = request.GET.get('ordenar_por', '')
    termo_busca = request.GET.get('busca', '').strip()

    opcoes_validas = {
        'data': 'data',
        'hora_inicio': 'hora_inicio',
        'hora_fim': 'hora_fim',
        'sala': 'sala__nome',
        'criador': 'criador__username',
        'nome': 'nome',
        'codigo_agendamento': 'codigo_agendamento',
    }

    campo_ordenacao = opcoes_validas.get(ordenar_por, 'data')  # padrão: data

    agendamentos = Agendamento.objects.filter(criador=request.user)

    if termo_busca:
        agendamentos = agendamentos.filter(
            Q(nome__icontains=termo_busca) |
            Q(criador__username__icontains=termo_busca) |
            Q(sala__nome__icontains=termo_busca) |
            Q(status__icontains=termo_busca) |
            Q(data__icontains=termo_busca)
        )

    agendamentos = agendamentos.order_by(campo_ordenacao)

    if is_admin(request.user):
        template_name = 'admin/agendamentos_admin.html'
    else:
        template_name = 'agendamentos_usuario.html'


    return render(request, template_name, {
        'agendamentos': agendamentos,
        'form': form,
        'ordenar_por': ordenar_por,
        'busca': termo_busca,
    })
    

@login_required
@require_POST
@csrf_protect
def criar_agendamento(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido.'}, status=405)

    form = AgendamentoForm(request.POST)
    if form.is_valid():
        agendamento = form.save(commit=False)
        if request.user.is_authenticated:
            agendamento.criador = request.user
        agendamento.save()
        form.save_m2m()  # salva usuários many-to-many

        # Retorna dados do novo agendamento (formate conforme necessário)
        return JsonResponse({
            'success': True,
            'agendamento': {
                'codigo_agendamento': getattr(agendamento, 'codigo_agendamento', agendamento.pk),                
                'nome': agendamento.nome,
                'sala': str(agendamento.sala),
                'criador': agendamento.criador.username if agendamento.criador else None,
                'data': agendamento.data.strftime('%d/%m/%Y') if agendamento.data else None,
                'hora_inicio': agendamento.hora_inicio.strftime('%H:%M') if agendamento.hora_inicio else None,
                'hora_fim': agendamento.hora_fim.strftime('%H:%M') if agendamento.hora_fim else None,
            }
        })
    else:
        # converte ErrorDict -> dict de listas para JSON
        print("Erros no formulário:", form.errors)
        errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)
    
def is_admin(user):
    return user.is_superuser or user.tipo_usuario == 'Admin'


@login_required
def editar_perfil(request, user_id=None):
    if user_id and is_admin(request.user):
        usuario = get_object_or_404(Usuario, pk=user_id)
        is_self = usuario == request.user
    else:
        usuario = request.user
        is_self = True

    if request.method == "POST":
        if "salvar_dados" in request.POST:
            form = UsuarioForm(request.POST, instance=usuario, user=request.user)
            if form.is_valid():
                if not is_admin(request.user):
                    form.instance.tipo_usuario = usuario.tipo_usuario
                form.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

        elif "alterar_senha" in request.POST:
            senha_form = CustomPasswordChangeForm(user=usuario, data=request.POST)
            if senha_form.is_valid():
                senha_form.save()
                update_session_auth_hash(request, usuario)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': senha_form.errors})

    # GET
    form = UsuarioForm(instance=usuario, user=request.user)
    senha_form = CustomPasswordChangeForm(user=usuario)
    if is_admin(request.user):
        template_name = 'admin/perfil_admin.html'
    else:
        template_name = 'perfil.html'

    return render(request, template_name, {
        'form': form,
        'senha_form': senha_form,
        'titulo': f"Editar Perfil - {usuario.username}" if not is_self else "Meu Perfil",
        'usuario_alvo': usuario,
        'is_admin': is_admin(request.user),
        'is_self': is_self,
    })
    
@login_required
def detalhes_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    pode_editar = agendamento.criado_por == request.user
    form = AgendamentoForm(instance=agendamento) if pode_editar else None

    if request.method == "POST" and pode_editar:
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "success": True,
                "id": agendamento.id,
                "message": "Agendamento atualizado com sucesso!",
                "titulo": agendamento.titulo,
                "data": agendamento.data.strftime("%d/%m/%Y"),
                "horario": str(agendamento.horario)
            })
        return JsonResponse({"success": False, "errors": form.errors})

    context = {"agendamento": agendamento, "pode_editar": pode_editar, "form": form}

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "modal_agendamento.html", context)

    return render(request, "index.html", context)