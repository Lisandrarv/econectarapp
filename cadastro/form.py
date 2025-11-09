from django import forms
from cadastro.models import Cadastro

class CadastrarForm(forms.ModelForm):

    class Meta:
        model = Cadastro
        fields = [
            'nome', 
            'email',
            'telefone',
            'endereco',
            'bairro',
            'password',
        ]
        widgets = {
            # Você pode usar um widget de PasswordInput para o campo 'password'
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class EntrarForm(forms.Form):
    # Este é um Form normal, não ModelForm, mas também deve usar 'password'
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # 🚨 MUDANÇA CRÍTICA: Substitua 'senha' por 'password'
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    
        