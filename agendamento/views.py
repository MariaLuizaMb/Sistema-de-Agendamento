from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from .models import Agendamento

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def home(request):
    """Página principal com listagem, filtro e pesquisa de agendamentos."""

    ordenar_por = request.GET.get('ordenar_por', '')
    termo_busca = request.GET.get('busca', '').strip()

    opcoes_validas = {
        'data': 'data',
        'hora_inicio': 'hora_inicio',
        'hora_fim': 'hora_fim',
        'sala': 'sala__nome',
        'criador': 'criador__username',
        'status': 'status',
        'nome': 'nome',
    }

    campo_ordenacao = opcoes_validas.get(ordenar_por, 'data')

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
        'ordenar_por': ordenar_por,
        'busca': termo_busca,
    })
