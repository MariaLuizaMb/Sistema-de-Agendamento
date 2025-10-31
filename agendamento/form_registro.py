from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
            "placeholder": "Senha",
            "autocomplete": "new-password",
            "required": True
        }),
        label="Senha"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
            "placeholder": "Confirmar senha",
            "autocomplete": "new-password",
            "required": True
        }),
        label="Confirmar senha"
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'cargo', 'tipo_usuario')

        widgets = {
            'username': forms.TextInput(attrs={
                "class": "bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
                "placeholder": "Nome de Usuário",
                "autocomplete": "name",
                "required": True
            }),
            'email': forms.EmailInput(attrs={
                "class": "bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md placeholder:text-darkBlue-50",
                "placeholder": "seu@email.com",
                "autocomplete": "email",
                "required": True
            }),
            'cargo': forms.Select(attrs={
                "class": "bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md text-darkBlue-50"
            }),
            #'tipo_usuario': forms.Select(attrs={
            #    "class": "bg-darkBlue-400 w-11/12 h-12 px-4 rounded-md text-darkBlue-50"
            #}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise ValidationError("Senhas não conferem.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
