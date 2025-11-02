from django import forms
from .models import Agendamento, Usuario

class AgendamentoForm(forms.ModelForm):
    # Campo de múltiplos usuários (participantes)
    usuarios = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(),
        required=True,
        label="Participantes",
        widget=forms.SelectMultiple(attrs={
            'class': 'bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50',
            'id': 'usuarios',
            'placeholder': 'Participantes'
            'multiple'
        })
    )

    class Meta:
        model = Agendamento
        fields = ['nome', 'usuarios', 'data', 'hora_inicio', 'hora_fim', 'sala']

        widgets = {
            # Campo: Nome da reunião
            'nome': forms.TextInput(attrs={
                'class': 'bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50',
                'placeholder': 'Nome da reunião',
                'id': 'nome',
                'autocomplete': 'off'
            }),
            # Campo: Data da reunião
            'data': forms.DateInput(attrs={
                'class': 'bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md text-darkBlue-50',
                'type': 'date',
                'id': 'data'
            }),
            # Campo: Hora de início
            'hora_inicio': forms.TimeInput(attrs={
                'class': 'bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md text-darkBlue-50',
                'type': 'time',
                'id': 'hora_inicio'
            }),
            # Campo: Hora de término
            'hora_fim': forms.TimeInput(attrs={
                'class': 'bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md text-darkBlue-50',
                'type': 'time',
                'id': 'hora_fim'
            }),
            # Campo: Sala da reunião
            'sala': forms.Select(attrs={
                'class': 'bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md text-darkBlue-50',
                'id': 'sala'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Personaliza os rótulos (labels) e define mensagens de erro mais amigáveis.
        """
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome da reunião"
        self.fields['usuarios'].label = "Participantes"
        self.fields['data'].label = "Data"
        self.fields['hora_inicio'].label = "Hora de início"
        self.fields['hora_fim'].label = "Hora de término"
        self.fields['sala'].label = "Sala"

        # Define mensagens de erro personalizadas (para exibição no modal)
        for field_name, field in self.fields.items():
            field.error_messages = {
                'required': f'O campo {field.label.lower()} é obrigatório.',
                'invalid': f'O valor inserido em {field.label.lower()} não é válido.'
            }
