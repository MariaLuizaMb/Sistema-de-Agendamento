from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db.models import Q
from .models import Agendamento, Usuario
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .form_agendamento import AgendamentoForm
from .form_registro import RegisterForm

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

    return render(request, 'index.html', {
        'agendamentos': agendamentos,
        'form': form,
        'ordenar_por': ordenar_por,
        'busca': termo_busca,
    })


login_required
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
        errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)