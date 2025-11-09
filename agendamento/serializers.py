from rest_framework import serializers
from .models import Agendamento, Cooperativa # Importe os Models que você precisa

# Serializer para o Model Cooperativa
class CooperativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cooperativa
        fields = ['id', 'nome', 'endereco'] # Campos que você quer expor

# Serializer para o Model Agendamento (Este será o principal)
class AgendamentoSerializer(serializers.ModelSerializer):
    # Usar o Serializer da Cooperativa para ter o nome no JSON
    cooperativa = CooperativaSerializer(read_only=True)
    
    # Adicionar o nome da cooperativa na hora de CRIAR o agendamento via API (writeable)
    cooperativa_id = serializers.PrimaryKeyRelatedField(
        queryset=Cooperativa.objects.all(),
        source='cooperativa',
        write_only=True,
        allow_null=False
    )
    
    class Meta:
        model = Agendamento
        # Lista de campos que serão incluídos no JSON da API.
        # Note que 'cooperativa' é a FK (apenas para leitura) e 'cooperativa_id' para escrita.
        fields = (
            'id', 'usuario', 'nome', 'email', 'endereco', 'bairro', 
            'data', 'hora', 'observacao', 'status', 
            'cooperativa', 'cooperativa_id'
        )
        read_only_fields = ('usuario', 'nome', 'email', 'endereco', 'bairro')
        