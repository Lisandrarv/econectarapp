from django.shortcuts import render
from django.urls import reverse

def inicio(request):
    dados = []
    # Cada item dado aqui gerará um quadro no template inicial.
    dados.append(
        {
            'titulo' : 'Agende sua coleta',
            'descricao' : 'Encontre a cooperativa ideal para sua reciclagem e agende a coletar',
            'link': reverse('agendamento:agendar_coleta')
        }
    )
    dados.append(
        {
            'titulo' : 'Sua contribuição',
            'descricao' : 'Verifique o quanto você já reciclou e ajudou o meio ambiente',
            'link' : reverse('reciclagem')
        }
    )
    contexto = {
        'dados' : dados
    }
    return render(request, 'inicio.html', contexto)
