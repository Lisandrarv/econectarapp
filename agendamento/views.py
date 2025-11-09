from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.urls import reverse
from .form import AgendamentoForm
from .models import Agendamento
from cadastro.models import Cadastro 
from reciclagem.models import Cooperativa, PontoColeta
from django.template.loader import render_to_string # 🚨 NOVO IMPORT
from django.core.mail import send_mail # 🚨 NOVO IMPORT
from rest_framework import viewsets
from .serializers import AgendamentoSerializer
from django.db.models import Q # para filtros
from .models import Cooperativa # Certifique-se de importar o Model Cooperativa
from .serializers import CooperativaSerializer # Certifique-se de importar o Serializer


# 🚨 COMENTÁRIO: A função login_required_custom NÃO é mais necessária.
#    O decorator @login_required nativo do Django é muito mais seguro e confiável.
#    Eu removi essa função e usei apenas o @login_required nas Views abaixo.


# --- Dashboard (Página Pós-Login) ---
# Usando o decorator padrão do Django
@login_required
def dashboard(request):
    
    bairro_do_usuario = "Não definido"
    usuario_nome = request.user.email  # Usa o email como padrão
    agendamentos_futuros = Agendamento.objects.none()

    # --- Lógica para Obter Bairro e Nome ---
    try:
        # request.user JÁ É o objeto Cadastro (pois AUTH_USER_MODEL='cadastro.Cadastro')
        bairro_temp = request.user.bairro.strip() if request.user.bairro else None
        
        if bairro_temp:
            bairro_do_usuario = bairro_temp
            
        usuario_nome = request.user.nome if request.user.nome else request.user.email
        
    except AttributeError:
        # Se request.user não tiver 'bairro' (caso improvável, mas para segurança)
        pass 
    
    # --- Lógica de Filtragem ---
    if bairro_do_usuario != "Não definido":
        # Busca agendamentos futuros para este usuário (filtrando pelo BAIRRO)
        agendamentos_futuros = Agendamento.objects.filter(
            bairro__iexact=bairro_do_usuario, 
            data__gte=date.today()
        ).order_by('data', 'hora')
    
    # Se o bairro for "Não definido", agendamentos_futuros permanece vazio (objects.none())

    contexto = {
        'usuario_nome': usuario_nome,
        'bairro_cliente': bairro_do_usuario,
        'agendamentos_futuros': agendamentos_futuros,
    }
    
    return render(request, 'agendamento/dashboard.html', contexto)


# Agendamento (Com Lógica GET/POST e Filtro de Bairro) ---
@login_required
def agendar_coleta(request):
    
    # 1. Tenta obter o bairro do usuário (que é o objeto Cadastro)
    bairro_usuario = None
    try:
        # request.user JÁ É o objeto Cadastro
        bairro_temp = request.user.bairro.strip() if request.user.bairro else None
        if bairro_temp:
            bairro_usuario = bairro_temp
    except AttributeError:
        pass

    cooperativas_disponiveis = Cooperativa.objects.none()
    mensagem = "Seu bairro não está cadastrado ou o perfil é inválido. Verifique seus dados de cadastro."
    
    # 2. Lógica do Filtro (GET e POST usam a mesma lista)
    if bairro_usuario:
        cooperativas_disponiveis = Cooperativa.objects.filter(bairro__iexact=bairro_usuario)
        
        if cooperativas_disponiveis.exists():
            mensagem = f"Cooperativas disponíveis no seu bairro ({bairro_usuario})."
        else:
            mensagem = f"Nenhuma cooperativa encontrada no bairro {bairro_usuario}."

    
    if request.method == 'POST':
        # 🚨 Lógica POST para salvar o agendamento
        form = AgendamentoForm(request.POST)
        
        # O ID da cooperativa vem do campo radio no template
        coop_id = request.POST.get('cooperativa_selecionada_id') 

        if form.is_valid() and cooperativas_disponiveis.exists() and coop_id:
            
            agendamento = form.save(commit=False)
            
            # O bloco try/except original que injetava dados foi usado para prevenir erros.
            # Vamos manter a injeção de dados, mas simplificar o try/except para focar no e-mail.
            
            # --- INJEÇÃO MANUAL DE DADOS (CRÍTICO) ---
            try:
                # 1. Bairro: Obtido do usuário logado
                agendamento.bairro = bairro_usuario
                
                # 2. Usuário: Obtido do request.user
                agendamento.usuario = request.user 
                
                # 3. Cooperativa: Busca o objeto Cooperativa
                cooperativa_selecionada = get_object_or_404(Cooperativa, id=coop_id)
                agendamento.cooperativa = cooperativa_selecionada 
                
                # 4. Dados do Usuário
                agendamento.nome = request.user.nome if request.user.nome else f"Usuário {request.user.pk}"
                agendamento.email = request.user.email
                agendamento.endereco = request.user.endereco
                
                agendamento.save()
            
            except Exception as e:
                # Trata qualquer erro inesperado ao salvar (ex: campo faltando)
                mensagem = f"Erro ao salvar agendamento: {e}"
                # Retorna aqui para não tentar enviar o e-mail ou redirecionar
                context = {
                    'cooperativas': cooperativas_disponiveis,
                    'bairro_usuario': bairro_usuario if bairro_usuario else "Não definido",
                    'mensagem': mensagem,
                    'form': form 
                }
                return render(request, 'agendamento/agendamento.html', context)
            
            
            # 🚨 INÍCIO DO NOVO BLOCO DE E-MAIL (APÓS O agendamento.save() BEM-SUCEDIDO)
            try:
                # 1. Montar o Contexto do E-mail
                email_contexto = {
                    'usuario_nome': request.user.nome if request.user.nome else request.user.email,
                    'agendamento': agendamento,
                }
                
                # 2. Renderizar o corpo do e-mail
                email_body = render_to_string(
                    'agendamento/email/confirmacao_agendamento.txt', 
                    email_contexto
                )
                
                # 3. Enviar o E-mail (CORRIGINDO A DIGITAÇÃO DE end_mail para send_mail)
                send_mail(
                    subject='Confirmação de Agendamento de Coleta',
                    message=email_body,
                    from_email='noreply@seusite.com', 
                    recipient_list=[agendamento.email], 
                    fail_silently=False,
                )
                
                print("\nE-mail de confirmação enviado para o console!\n")
                
            except Exception as e:
                # Trata falhas no envio do e-mail (APENAS loga, não impede o redirect de sucesso)
                print(f"\nERRO AO ENVIAR E-MAIL: {e}\n")


            # Redireciona para a página de sucesso (agora, alinhado corretamente)
            return redirect(reverse('agendamento:sucesso_agendamento')) 
            
        else:
            # Se o formulário for inválido ou faltar seleção
            mensagem = "Erro: Verifique os campos e certifique-se de ter selecionado uma Cooperativa."
    
    else:
        # Lógica GET: Cria um novo formulário (fora do POST)
        form = AgendamentoForm()

    context = {
        'cooperativas': cooperativas_disponiveis,
        'bairro_usuario': bairro_usuario if bairro_usuario else "Não definido",
        'mensagem': mensagem,
        'form': form 
    }
    
    # 🚨 Bloco de e-mail INEXISTENTE ou fora de lugar foi removido daqui

    return render(request, 'agendamento/agendamento.html', context)

@login_required 
def lista_agendamentos(request):
    
    # 🚨 CORREÇÃO CRÍTICA: Filtrar PELA RELAÇÃO DE USUÁRIO
    # O Model Agendamento tem um campo 'usuario' que é ForeignKey para o request.user
    agendamentos = Agendamento.objects.filter(
        usuario=request.user
    ).order_by('-data', '-hora')

    # A lógica de try/except e de buscar o 'cadastro' é desnecessária aqui,
    # pois o agendamento foi salvo com a FK correta para request.user.
    
    return render(request, 'agendamento/lista_agendamentos.html', {
        'agendamentos': agendamentos
    })
    
@login_required
def detalhe_agendamento(request, pk):
    
    # Busca o agendamento pelo ID (pk), mas SÓ se pertencer ao usuário logado
    agendamento = get_object_or_404(
        Agendamento, 
        pk=pk, 
        usuario=request.user # Garante que o usuário só veja seus próprios dados
    )

    contexto = {
        'agendamento': agendamento
    }
    
    return render(request, 'agendamento/detalhe_agendamento.html', contexto)

@login_required
def lista_pontos(request):
    
    # 1. Obter o bairro do usuário (que é o objeto Cadastro)
    bairro_usuario = None
    try:
        # request.user JÁ É o objeto Cadastro
        bairro_temp = request.user.bairro.strip() if request.user.bairro else None
        if bairro_temp:
            bairro_usuario = bairro_temp
    except AttributeError:
        pass

    pontos_disponiveis = PontoColeta.objects.none()
    mensagem = "Seu bairro não está cadastrado ou o perfil é inválido. Verifique seus dados de cadastro."

    # 2. Aplicar o filtro nos Pontos de Coleta
    if bairro_usuario:
        pontos_disponiveis = PontoColeta.objects.filter(bairro__iexact=bairro_usuario)
        if pontos_disponiveis.exists():
            mensagem = f"Pontos de Coleta disponíveis no seu bairro ({bairro_usuario})."
        else:
            mensagem = f"Nenhum ponto de coleta encontrado no bairro {bairro_usuario}."

    contexto = {
        'pontos': pontos_disponiveis,
        'bairro_usuario': bairro_usuario if bairro_usuario else "Não definido",
        'mensagem': mensagem,
    }
    
    # Renderiza o template de listagem de pontos
    return render(request, 'reciclagem/lista_pontos.html', contexto)

@login_required
def detalhe_ponto(request, pk):
    
    # Busca o ponto de coleta pelo ID (pk)
    # Não precisa filtrar por usuário, pois é informação pública (mas pode filtrar por bairro se desejar mais segurança)
    ponto = get_object_or_404(PontoColeta, pk=pk)

    contexto = {
        'ponto': ponto
    }
    
    # O template a ser criado será 'reciclagem/detalhe_ponto.html'
    return render(request, 'reciclagem/detalhe_ponto.html', contexto)

# 🚨 NOVA VIEW: Cancelamento de Agendamento
@login_required
def cancelar_agendamento(request, pk):
    agendamento = get_object_or_404(
        Agendamento, 
        pk=pk, 
        usuario=request.user # Garante que apenas o usuário logado possa cancelar o seu próprio agendamento
    )

    # Lógica de cancelamento: só permite cancelar se o status atual for 'AGENDADO'
    if agendamento.status == 'AGENDADO':
        agendamento.status = 'CANCELADO'
        agendamento.save()
        # Opcional: Adicionar uma mensagem de sucesso
        # messages.success(request, "Agendamento cancelado com sucesso.")
    
    # Redireciona de volta para a lista de agendamentos
    return redirect('agendamento:lista_agendamentos')

# --- Página de Sucesso (ESSENCIAL) ---
from django.shortcuts import render # Importar render se não estiver no topo

def sucesso_agendamento(request):
    return render(request, 'agendamento/sucesso_agendamento.html')

# 🚨 API VIEWSET PARA AGENDAMENTO
class AgendamentoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite agendamentos serem visualizados ou editados.
    Filtra agendamentos para mostrar apenas os do usuário logado.
    """
    serializer_class = AgendamentoSerializer
    
    # Garante que apenas o agendamento do usuário logado seja retornado
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Retorna todos os agendamentos do usuário logado
            return Agendamento.objects.filter(usuario=user).order_by('-data', '-hora')
        
        # Se não estiver logado, não retorna nada
        return Agendamento.objects.none()

    # Sobrescreve a criação para injetar o usuário logado e dados do cadastro
    def perform_create(self, serializer):
        # Injete os dados do usuário no serializer antes de salvar
        user = self.request.user
        serializer.save(
            usuario=user,
            nome=user.nome,
            email=user.email,
            endereco=user.endereco,
            bairro=user.bairro
        )
class CooperativaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint que permite Cooperativas serem visualizadas.
    (Apenas leitura, já que não queremos que usuários criem cooperativas)
    """
    queryset = Cooperativa.objects.all().order_by('nome')
    serializer_class = CooperativaSerializer       
