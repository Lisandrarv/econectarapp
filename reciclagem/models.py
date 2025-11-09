from django.db import models

class MaterialReciclavel(models.Model):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição')

    def __str__(self):
        return self.nome

class PontoColeta(models.Model):
    nome = models.CharField('Ponto de Coleta', max_length=200)
    endereco = models.CharField('Endereço', default= 'Não informado', max_length=100)
    numero = models.CharField('Numero', default= 'S/N', max_length=20)
    bairro = models.CharField('Bairro', max_length=100)
    horario_funcionamento = models.CharField('Horário de Funcionamento', default= 'S/N', max_length=255)
    tipos_aceitos = models.TextField('Tipos de Materiais Aceitos', default= 'Não especificado')
    telefone = models.CharField('Telefone', max_length=50, blank=True)

    def __str__(self):
        return self.nome

class Usuario (models.Model):
    nome = models.CharField('Nome Completo', max_length=70)
    email = models.EmailField('E-mail')
    endereco = models.CharField('Endereço', max_length=100)
    bairro = models.CharField('Bairro', max_length=100)
    senha = models.CharField('Senha', max_length=50)

    def __str__(self):
        return self.nome
    
class Cooperativa(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=20)
    bairro = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    horario_funcionamento = models.CharField('Horário de Funcionamento', default= 'S/N', max_length=255)
    tipos_aceitos = models.TextField('Tipos de Materiais Aceitos', default= 'Não especificado')

    def __str__(self):
        return self.nome
    
class CooperativaMaterial(models.Model):
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE)
    material = models.ForeignKey(MaterialReciclavel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cooperativa.nome} - {self.material.nome}"
    