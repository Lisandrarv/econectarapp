from django.urls import path
from . import views

app_name = 'agendamento'

urlpatterns = [
    path('', views.dashboard, name='dashboard'), # Página Inicial do Usuário (Dashboard)
    path('agendar/', views.agendar_coleta, name='agendar_coleta'), # Página para Agendar Coleta
    path('lista/', views.lista_agendamentos, name='lista_agendamentos'),
    path('lista/<int:pk>/', views.detalhe_agendamento, name='detalhe_agendamento'),
    path('pontos/', views.lista_pontos, name='lista_pontos'),
    path('sucesso/', views.sucesso_agendamento, name='sucesso_agendamento'), # Página de Sucesso
    path('pontos/<int:pk>/', views.detalhe_ponto, name='detalhe_ponto'),
    path('cancelar/<int:pk>/', views.cancelar_agendamento, name='cancelar_agendamento'),
]
