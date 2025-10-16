from django.contrib import admin
from .models import Usuario, Sala, Agendamento, AgendamentoUsuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'tipo_usuario', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('tipo_usuario', 'is_active')


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_sala', 'capacidade', 'criador')
    search_fields = ('nome',)
    list_filter = ('tipo_sala',)


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sala', 'data', 'hora_inicio', 'hora_fim', 'status', 'criador')
    list_display_links = ('nome',)
    
    list_filter = ('status', 'data', 'sala')
    search_fields = ('nome', 'sala__nome', 'criador__username')
    ordering = ('-data', 'hora_inicio')
    date_hierarchy = 'data'


@admin.register(AgendamentoUsuario)
class AgendamentoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('agendamento', 'usuario')
    search_fields = ('agendamento__nome', 'usuario__username')
