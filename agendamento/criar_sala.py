from django import forms
from .models import Sala


class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nome', 'capacidade', 'tipo_sala']

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50',
                'placeholder': 'Nome da sala',
                'id': 'nome_sala',
                'autocomplete': 'off'
            }),
            'capacidade': forms.NumberInput(attrs={
                'class': 'bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50',
                'placeholder': 'Capacidade',
                'min': '1',
                'id': 'capacidade'
            }),
            'tipo_sala': forms.Select(attrs={
                'class': 'bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md text-darkBlue-50',
                'id': 'tipo_sala'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].label = "Nome"
        self.fields['capacidade'].label = "Capacidade"
        self.fields['tipo_sala'].label = "Tipo da sala"

        for field_name, field in self.fields.items():
            field.error_messages = {
                'required': f'O campo {field.label.lower()} é obrigatório.',
                'invalid': f'O valor inserido em {field.label.lower()} não é válido.'
            }
