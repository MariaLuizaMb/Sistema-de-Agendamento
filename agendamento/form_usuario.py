from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name','username', 'email', 'cargo', 'tipo_usuario']
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
                "placeholder": "Primeiro Nome",
                "autocomplete": "given-name",
                "required": True
            }),
            'last_name': forms.TextInput(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
                "placeholder": "Último Nome",
                "autocomplete": "family-name",
                "required": True
            }),
            'username': forms.TextInput(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
                "placeholder": "Nome de Usuário",
                "autocomplete": "username",
                "required": True
            }),
            'email': forms.EmailInput(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
                "placeholder": "seu@email.com",
                "autocomplete": "email",
                "required": True
            }),
            'cargo': forms.Select(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md text-darkBlue-50"
            }),
            'tipo_usuario': forms.Select(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md text-darkBlue-50"
            }),
        }
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # usuário logado
        super().__init__(*args, **kwargs)

        # Desabilita campos para usuários não-admin
        if user and user.tipo_usuario != 'Admin':
            self.fields.pop('tipo_usuario')
            self.fields['cargo'].widget.attrs['readonly'] = True
            self.instance.cargo = self.instance.cargo



class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Senha atual',
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-lg border-gray-300 focus:ring-indigo-500 focus:border-indigo-500 p-2'
        })
    )
    new_password1 = forms.CharField(
        label='Nova senha',
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-lg border-gray-300 focus:ring-indigo-500 focus:border-indigo-500 p-2'
        })
    )
    new_password2 = forms.CharField(
        label='Confirmar nova senha',
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-lg border-gray-300 focus:ring-indigo-500 focus:border-indigo-500 p-2'
        })
    )
