from django.db import models
from django.contrib.auth import get_user_model
from reciclagem.models import Cooperativa # Importe Cooperativa se necessário

User = get_user_model() # Obtém o modelo de usuário ativo (seja Django ou Customizado)

class Agendamento(models.Model):
  # Adicionado: Relação com o Usuário (quem fez o agendamento)
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário'
    )
    
    # Adicionado: Relação com a Cooperativa/Ponto (quem fará a coleta)
    cooperativa = models.ForeignKey(
        Cooperativa,
        on_delete=models.CASCADE,
        verbose_name='Cooperativa/Ponto de Coleta'
    )
    
    # 🚨 NOVO CAMPO: Status do Agendamento
    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('CANCELADO', 'Cancelado pelo Usuário'),
        ('CONCLUIDO', 'Concluído'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='AGENDADO'
    )

    nome = models.CharField(verbose_name= 'Nome Completo', max_length=100)
    email = models.EmailField(verbose_name= 'E-mail')
    endereco = models.CharField(verbose_name= 'Endereço', max_length=100)
    bairro = models.CharField(verbose_name= 'Bairro', max_length=100)
    data = models.DateField(verbose_name= 'Data de Coleta')
    hora = models.TimeField(verbose_name= 'Hora da Coleta')
    observacao = models.CharField(verbose_name= 'Observação', max_length=999)
  
  
    def __str__(self):
        return f"Agendamento de {self.nome} em {self.data}"

# Create your models here.
