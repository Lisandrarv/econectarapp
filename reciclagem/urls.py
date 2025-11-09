from django.urls import path
from . import views

urlpatterns = [
    # Adicione rotas de reciclagem (como listagem de pontos) aqui mais tarde.
    # Exemplo: path('pontos/', views.listar_pontos, name='listar_pontos'),
    path('', views.pontos_view_reciclagem, name='reciclagem'), # <-- Nome Corrigido!
    path('buscar-cooperativas/', views.buscar_cooperativas, name='buscar_cooperativas'),
    path('detalhes-cooperativa/<int:cooperativa_id>/', views.detalhes_cooperativa, name='detalhes_cooperativa'),
    path('listar-pontos/', views.listar_pontos, name='listar_pontos'),
    path('detalhes-ponto/<int:ponto_id>/', views.detalhes_ponto, name='detalhes_ponto'),
    # NOVAS ROTAS DE CADASTRO (CREATE)
    path('cadastrar-ponto/', views.cadastrar_ponto, name='cadastrar_ponto'), # VIEW 'C' (CREATE - Ponto)
    path('cadastrar-cooperativa/', views.cadastrar_cooperativa, name='cadastrar_cooperativa'), # VIEW 'C' (CREATE - Cooperativa)
    
    # ... Rotas de Edição (Update) e Deleção (Delete) virão depois
    
]