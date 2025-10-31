from django import forms
from .models import Agendamento, Usuario

class AgendamentoForm(forms.ModelForm):
    usuarios = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Agendamento
        fields = ['nome', 'usuarios', 'data', 'hora_inicio', 'hora_fim', 'sala']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'sala': forms.Select(attrs={'class': 'form-control'}),
        }