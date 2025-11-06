from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone


class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('Admin', 'Admin'),
        ('Comum', 'Comum'),
    ]
    CARGO_CHOICES = [
        ('Diretor', 'Diretor'),
        ('Gerente', 'Gerente'),
        ('Coordenador', 'Coordenador'),
        ('Funcionario', 'Funcionário'),
    ]
    email = models.EmailField(unique=True, blank=False, null=False)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_CHOICES, default='Comum')
    cargo = models.CharField(max_length=100, choices=CARGO_CHOICES, blank=False, null=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"


class Sala(models.Model):
    TIPO_CHOICES = [
        ('Sala de Reunião', 'Sala de Reunião'),
        ('Sala de Trabalho', 'Sala de Trabalho'),
        ('Sala de Videochamada', 'Sala de Videochamada'),
        ('Sala de Brainstorming', 'Sala de Brainstorming'),
        ('Sala Genérica', 'Sala Genérica'),
    ]

    nome = models.CharField(max_length=100, unique=True)
    capacidade = models.PositiveIntegerField()
    tipo_sala = models.CharField(max_length=30, choices=TIPO_CHOICES)
    criador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,  # se admin for apagado, a sala continua
        null=True,
        blank=True,
        related_name="salas_criadas"
    )

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_sala_display()})"


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('cancelado', 'Cancelado'),
    ]

    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='agendamentos')
    criador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,  # se admin sair, reunião não some
        null=True,
        blank=True,
        related_name="agendamentos_criados"
    )
    nome = models.CharField(max_length=100, verbose_name="Nome da Reunião")
    usuarios = models.ManyToManyField(Usuario, through='AgendamentoUsuario')
    data = models.DateField(verbose_name="Data da Reunião")
    hora_inicio = models.TimeField(verbose_name="Hora de Início")
    hora_fim = models.TimeField(verbose_name="Hora de Término")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    codigo_agendamento = models.CharField(max_length=20, unique=True, blank=True, null=True)

    class Meta:
        unique_together = ('sala', 'data', 'hora_inicio', 'hora_fim')
        ordering = ['data', 'hora_inicio']

    def __str__(self):
        return f"{self.nome} - {self.sala.nome} ({self.data:%d/%m/%Y}, {self.hora_inicio:%H:%M} às {self.hora_fim:%H:%M})"

    def clean(self):
        """Validação personalizada de horários e conflitos."""
        # Hora de término deve ser posterior à de início
        if self.hora_fim <= self.hora_inicio:
            raise ValidationError("A hora de término deve ser posterior à hora de início.")

        # Não permitir agendamentos no passado
        agora = timezone.localtime()
        data_hora_inicio = timezone.make_aware(
            timezone.datetime.combine(self.data, self.hora_inicio)
        )
        if data_hora_inicio < agora:
            raise ValidationError("Não é possível criar agendamentos no passado.")

        # Verificação de conflitos
        conflitos = Agendamento.objects.filter(
            sala=self.sala,
            data=self.data,
            status='ativo'
        ).exclude(pk=self.pk).filter(
            hora_inicio__lt=self.hora_fim,
            hora_fim__gt=self.hora_inicio
        )

        if conflitos.exists():
            raise ValidationError("Já existe um agendamento que conflita com este horário.")

    def save(self, *args, **kwargs):
        self.full_clean()
        is_new = self.pk is None

        super().save(*args, **kwargs)

        # Se for um agendamento novo e ainda não tem código
        if is_new and self.criador and not self.codigo_agendamento:
            self.codigo_agendamento = f"{self.criador.id:02d}{self.id:02d}"
            super().save(update_fields=['codigo_agendamento'])


class AgendamentoUsuario(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('agendamento', 'usuario')
        

    def __str__(self):
        return f"{self.usuario.username} em {self.agendamento}"
