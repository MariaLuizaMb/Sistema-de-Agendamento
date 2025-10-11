from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Sala, Agendamento, AgendamentoUsuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('id', 'username', 'email', 'tipo_usuario', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

    # Adiciona o campo tipo_usuario nos formulários de edição/criação
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('tipo_usuario',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('tipo_usuario',)}),
    )


class AgendamentoUsuarioInline(admin.TabularInline):
    model = AgendamentoUsuario
    extra = 1


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'sala', 'data', 'hora_inicio', 'hora_fim', 'status', 'criador')
    list_filter = ('sala', 'data', 'status')
    search_fields = ('sala__nome', 'criador__username', 'criador__email')
    inlines = [AgendamentoUsuarioInline]


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'capacidade', 'tipo_sala', 'criador')
    list_filter = ('tipo_sala',)
    search_fields = ('nome', 'criador__username', 'criador__email')


@admin.register(AgendamentoUsuario)
class AgendamentoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'agendamento', 'usuario')
    search_fields = ('agendamento__sala__nome', 'usuario__username', 'usuario__email')
