from django.contrib import admin
from .models import Cooperativa, Agendamento # Importe os models necessários

# 🚨 1. Registrar o Model Cooperativa
@admin.register(Cooperativa)
class CooperativaAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na lista de cooperativas no Admin
    list_display = ('nome', 'bairro', 'endereco', 'horario_funcionamento')
    # Campos que poderão ser pesquisados
    search_fields = ('nome', 'bairro')
    pass
    
# 🚨 2. (Opcional) Registrar o Model Agendamento para facilitar a visualização
@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'usuario', 'bairro', 'data', 'status', 'cooperativa')
    list_filter = ('status', 'bairro', 'cooperativa')
    search_fields = ('usuario__email', 'bairro', 'pk')
    # Permite editar campos na lista (apenas para campos não sensíveis)
    list_editable = ('status',)
# Register your models here.
