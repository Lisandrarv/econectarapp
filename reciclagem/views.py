from django.shortcuts import render, redirect
from reciclagem.models import MaterialReciclavel, PontoColeta, Usuario, Cooperativa, CooperativaMaterial
from .models import PontoColeta, Cooperativa
from .forms import PontoColetaForm, CooperativaForm

def get_usuario_bairro(request):
    # Supondo que o usuário esteja autenticado e você tenha um modelo de usuário com o campo 'bairro'
    if request.user.is_authenticated:
        try:
            usuario = Usuario.objects.get(email=request.user.email)
            return usuario.bairro
        except Usuario.DoesNotExist:
            return None
    return None


def buscar_servicos_por_bairro(request):
    bairro_do_usuario = get_usuario_bairro(request)
    if not bairro_do_usuario:
        return render(request, 'reciclagem/resultado.html', {
            'pontos_proximos': [],
            'cooperativas_proximas': [],
            'bairro': 'Não encontrado'
        })

    pontos_proximos = PontoColeta.objects.filter(bairro__iexact=bairro_do_usuario) 
    cooperativas_proximas = Cooperativa.objects.filter(bairro__iexact=bairro_do_usuario)
    
    contexto = {
        'bairro': bairro_do_usuario,
        'cooperativas_proximas': cooperativas_proximas,
        'pontos_proximos': pontos_proximos,
    }
    return render(request, 'reciclagem/resultado.html', contexto)

def pontos_view_reciclagem(request):

    return render(request, 'reciclagem/pontos.html', {})
    
def reciclagem(request):
    query = request.GET.get('q', '')
    # lista de pontos para autocomplete

    pontos = PontoColeta.objects.all().values_list('nome', 'bairro', 'endereco')
    results = []
    if query:
        results = MaterialReciclavel.objects.filter(nome__icontains=query)
    return render(request, 'reciclagem.html', {
        'results': results,
        'pontos': pontos,
        'query': query
    })
    bairro = models.CharField('Bairro', max_length=100)
    
def cooperativas(request):
    cooperativas = None
    bairro = Cooperativa.objects.values_list('bairro', flat=True).distinct()
    materiais = MaterialReciclavel.objects.all()
    
    
    if request.method == 'GET':
            bairro = request.GET.get('bairro')
            material_ids = request.GET.getlist('materiais')
            
            cooperativas = Cooperativa.objects.filter()
            if bairro:
                cooperativas = cooperativas.filter(bairro=bairro)
            if material_ids:
                cooperativas = cooperativas.filter(
                    id__in=CooperativaMaterial.objects.filter(
                        material_id__in=material_ids
                    ).values_list('cooperativa_id', flat=True)
                ).distinct()
    return render(request, 'cooperativas.html', {
        'cooperativas': cooperativas,
        'bairros': bairros,
        'materiais': materiais
    })
def detalhes_cooperativa(request, cooperativa_id):
    cooperativa = Cooperativa.objects.get(id=cooperativa_id)
    materiais = MaterialReciclavel.objects.filter(
        id__in=CooperativaMaterial.objects.filter(
            cooperativa=cooperativa
        ).values_list('material_id', flat=True)
    )
    return render(request, 'detalhes_cooperativa.html', {
        'cooperativa': cooperativa,
        'materiais': materiais
    })          
    def __str__(self):
        return self.nome
    
def buscar_cooperativas(request):
    bairro = Cooperativa.objects.values_list('bairro', flat=True).distinct()
    materiais = MaterialReciclavel.objects.all()
    cooperativas = None

    if request.method == 'GET':
        bairro = request.GET.get('bairro')
        material_ids = request.GET.getlist('materiais')

        cooperativas = Cooperativa.objects.all()
        if bairro:
            cooperativas = cooperativas.filter(bairro=bairro)
        if material_ids:
            cooperativas = cooperativas.filter(
                id__in=CooperativaMaterial.objects.filter(
                    material_id__in=material_ids
                ).values_list('cooperativa_id', flat=True)
            ).distinct()

    return render(request, 'buscar_cooperativas.html', {
        'cooperativas': cooperativas,
        'bairro': bairro,
        'materiais': materiais
    }) 
     
    def detalhes_ponto(request, ponto_id):
        ponto = PontoColeta.objects.get(id=ponto_id)
        materiais = MaterialReciclavel.objects.filter(
            id__in=ponto.materiais.values_list('id', flat=True)
        )

        return render(request, 'detalhes_ponto.html', {
            'ponto': ponto,
            'materiais': materiais
        })
# reciclagem/views.py

# from .models import PontoColeta, Cooperativa # Adicione este import quando for usar os models


def listar_pontos(request):
    # Lógica de processamento de dados pode vir aqui.
    # Exemplo:
    pontos = PontoColeta.objects.all().order_by('bairro', 'nome')
    cooperativas = Cooperativa.objects.all().order_by('bairro', 'nome')

    contexto = {
        'pontos': pontos, # Deve ser 'pontos'
        'cooperativas': cooperativas, # Deve ser 'cooperativas'
        'titulo': 'Pontos de Coleta e Cooperativas Registradas'
    }
    # O template que acabamos de criar
    return render(request, 'reciclagem/pontos.html', contexto)

def detalhes_ponto(request, ponto_id):
    ponto = PontoColeta.objects.get(id=ponto_id)
    materiais = MaterialReciclavel.objects.filter(
        id__in=ponto.materiais.values_list('id', flat=True)
    )

    return render(request, 'detalhes_ponto.html', {
        'ponto': ponto,
        'materiais': materiais
    })
    
    # ----------------------------------------------------------------------
# 1. CRUD de PontoColeta (Pontos)
# ----------------------------------------------------------------------

# A. CREATE: Cadastrar Novo Ponto de Coleta
# Vamos proteger esta rota com um login simples por enquanto, assumindo que só admins/gestores podem criar.
def cadastrar_ponto(request):
    if request.method == 'POST':
        form = PontoColetaForm(request.POST)
        if form.is_valid():
            form.save()
            # Retorna para a lista após salvar
            # messages.success(request, 'Ponto de Coleta cadastrado com sucesso!')
            return redirect('listar_pontos') 
    else:
        form = PontoColetaForm()
        
    return render(request, 'reciclagem/cadastrar_ponto.html', {'form': form, 'titulo': 'Cadastrar Novo Ponto de Coleta'})

# ----------------------------------------------------------------------
# 2. CRUD de Cooperativa
# ----------------------------------------------------------------------

# A. CREATE: Cadastrar Nova Cooperativa
def cadastrar_cooperativa(request):
    if request.method == 'POST':
        form = CooperativaForm(request.POST)
        if form.is_valid():
            form.save()
            # Retorna para a lista de pontos por conveniência
            # messages.success(request, 'Cooperativa cadastrada com sucesso!')
            return redirect('listar_pontos') 
    else:
        form = CooperativaForm()
        
    return render(request, 'reciclagem/cadastrar_cooperativa.html', {'form': form, 'titulo': 'Cadastrar Nova Cooperativa'})

