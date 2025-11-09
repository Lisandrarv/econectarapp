from django import forms
from .models import PontoColeta, Cooperativa

# Formulário para Ponto de Coleta
class PontoColetaForm(forms.ModelForm):
    class Meta:
        model = PontoColeta
        # Campos que o usuário irá preencher
        fields = ['nome', 'bairro', 'endereco', 'numero', 'horario_funcionamento', 'tipos_aceitos']
        # Definindo classes CSS para Bootstrap
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'horario_funcionamento': forms.TextInput(attrs={'class': 'form-control'}),
            'tipos_aceitos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formulário para Cooperativa
class CooperativaForm(forms.ModelForm):
    class Meta:
        model = Cooperativa
        # Campos que o usuário irá preencher
        fields = ['nome', 'endereco', 'bairro','numero', 'telefone']
        # Definindo classes CSS para Bootstrap
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'horario_funcionamento': forms.TextInput(attrs={'class': 'form-control'}),
            'tipos_aceitos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }