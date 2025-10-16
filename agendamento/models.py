from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('Admin', 'Admin'),
        ('Comum', 'Comum'),
    ]
    email = models.EmailField(unique=True)  # Torna o email único
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_CHOICES, default='Comum')   

    def __str__(self):
        return f"{self.username} ({self.tipo_usuario})"


class Sala(models.Model):
    TIPO_CHOICES = [
        ('reuniao', 'Sala de Reunião'),
        ('trabalho', 'Sala de Trabalho'),
        ('videochamada', 'Sala de Videochamada'),
        ('brainstorming', 'Sala de Brainstorming'),
        ('generica', 'Sala Genérica'),
    ]

    nome = models.CharField(max_length=100, unique=True)
    capacidade = models.PositiveIntegerField()
    tipo_sala = models.CharField(max_length=20, choices=TIPO_CHOICES)
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
    data = models.DateField()
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')

    class Meta:
        unique_together = ('sala', 'data', 'hora_inicio', 'hora_fim')

    def __str__(self):
        return f"{self.nome} - {self.sala.nome} ({self.data} {self.hora_inicio}-{self.hora_fim})"

    def clean(self):
        # Verifica conflito de horários
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
        self.full_clean()  # validação antes de salvar
        super().save(*args, **kwargs)


class AgendamentoUsuario(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('agendamento', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} em {self.agendamento}"
