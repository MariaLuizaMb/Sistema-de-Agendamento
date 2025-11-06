from django import forms
from .models import Usuario


class CriarUsuario(forms.ModelForm):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": "bg-white w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
            "placeholder": "Digite uma senha",
            "required": True
        })
    )
    password2 = forms.CharField(
        label="Confirme a senha",
        widget=forms.PasswordInput(attrs={
            "class": "bg-white w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
            "placeholder": "Confirme a senha",
            "required": True
        })
    )

    class Meta:
        model = Usuario
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'cargo',
            'tipo_usuario',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
                "placeholder": "Primeiro Nome",
            }),
            'last_name': forms.TextInput(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
                "placeholder": "Último Nome",
            }),
            'username': forms.TextInput(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
                "placeholder": "Nome de Usuário",
            }),
            'email': forms.EmailInput(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
                "placeholder": "seu@email.com",
            }),
            'cargo': forms.Select(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md text-darkBlue-50"
            }),
            'tipo_usuario': forms.Select(attrs={
                "class": "bg-white w-11/12 h-12 px-4 rounded-md text-darkBlue-50"
            }),
        }

    def clean(self):
        """Valida se as senhas coincidem."""
        cleaned_data = super().clean()
        senha1 = cleaned_data.get("password1")
        senha2 = cleaned_data.get("password2")

        if senha1 and senha2 and senha1 != senha2:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        """Cria o usuário com senha criptografada."""
        usuario = super().save(commit=False)
        senha = self.cleaned_data.get("password1")
        if senha:
            usuario.set_password(senha)
        if commit:
            usuario.save()
        return usuario
