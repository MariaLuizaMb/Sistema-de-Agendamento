from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Sala, Agendamento, AgendamentoUsuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('username', 'first_name', 'last_name', 'cargo', 'tipo_usuario')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'cargo', 'tipo_usuario', 'is_staff', 'is_active')}
        ),
    )
    list_display = ('email', 'username', 'tipo_usuario', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_sala', 'capacidade', 'criador')
    search_fields = ('nome',)
    list_filter = ('tipo_sala',)
    
class AgendamentoUsuarioInline(admin.TabularInline):
    """Permite adicionar vários usuários dentro do agendamento."""
    model = AgendamentoUsuario
    extra = 1


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('codigo_agendamento', 'nome', 'sala', 'data', 'hora_inicio', 'hora_fim', 'status', 'criador')
    list_filter = ('status', 'sala', 'data')
    search_fields = ('codigo_agendamento', 'nome', 'sala__nome', 'criador__username')
    inlines = [AgendamentoUsuarioInline]
    ordering = ('-data', '-hora_inicio')
    date_hierarchy = 'data'
    readonly_fields = ('codigo_agendamento',)


@admin.register(AgendamentoUsuario)
class AgendamentoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('agendamento', 'usuario')
    search_fields = ('agendamento__nome', 'usuario__username')
