# Econectar 
🌱 Projeto de um aplicativo web feito com Django que conecta usuários a pontos de coleta de materiais recicláveis, promove agendamentos de coleta e reforça a educação ambiental com uma inteface moderma.

Os serviços disponíveis são:

* Agendamento de coleta
* Localização de pontos de coleta
* Contato com Cooperativas
* Autenticação
* Feedback ambiental

<div align="center">


### Objetivo

Criar um aplicativo de coleta de materiais recicláveis que busca conscientizar sobre a importância da reciclagem do lixo, auxiliando a população da cidade de Porto Alegre na identificação dos tipos de materiais recicláveis e as formas corretas de reciclagem, trazendo informações sobre rotas de coleta de lixo, assim como empresas de coletas de materiais recicláveis específicos.


### Demonstração da solução

Protótipos Interativos: A seguir, são apresentados os protótipos de interface do aplicativo, criados no Figma. Eles ilustram as telas e interações dos módulos de login de Pessoas Físicas, agendamento e localização de pontos de coleta. Para visualizar os protótipos
interativos, basta clicar nos links abaixo.

<img src="https://github.com/Lucas-sgarioni/econectar/blob/6299098dafee292e3b2cf0fadc69ebe60553d2c8/assets/img/Tela%20login.png">
<img src="https://github.com/Lucas-sgarioni/econectar/blob/6299098dafee292e3b2cf0fadc69ebe60553d2c8/assets/img/Agendamento%20da%20coleta.png">
<img src="https://github.com/Lucas-sgarioni/econectar/blob/6299098dafee292e3b2cf0fadc69ebe60553d2c8/assets/img/Meus%20agendamentos.png">
<img src="https://github.com/Lucas-sgarioni/econectar/blob/6299098dafee292e3b2cf0fadc69ebe60553d2c8/assets/img/Minhas%20reciclagens.png">
<img src="https://github.com/Lucas-sgarioni/econectar/blob/6299098dafee292e3b2cf0fadc69ebe60553d2c8/assets/img/Fluxo%20das%20telas.png">
</div>

### ⚙️ Pré-requisitos:
Antes de executar o projeto instale:
* Python 3.9+
* Pip
* Git
* Um ambiente virtual (recomendado: venv ou virtualenv)

### 🚀 Como executar o projeto localmente:
1. Clonar o repositório:
git clone https://github.com/seu-usuario/econectar.git
cd econectar

2. Criar um ambiente vitual:
python -m venv venv

3. Ativar o ambiente virtual:
   * Windows
     venv\Scripts\activate

4. Instalar as dependências:
pip install -r requirements.txt
Criar o arquivo requirements se ele não exisitir:
pip freeze > requirements.txt

5. Realizar as migrações:
python manage.py makemigrations
python manage.py migrate

6. Iniciar o servidor:
python manage.py runserver

7. Acessar o servidor:
Acesse em http://127.0.0.1:8000

### 🗃️ Scripts de Carga (dados iniciais)
Este é um script com dados de exemplo, com instruções, para os pontos de coleta ou agendamentos:
python manage.py loaddata coleta/fixtures/pontos_coleta.json

### ☁️ Subida para Nuvem (opcional)
Se for implantar o projeto em ambiente de nuvem (como Heroku, Railway ou Render), inclua:

  * Procfile
  * runtime.txt
  * requirements.txt
  * Configuração para STATICFILES

### Tecnologias Utilizadas

* Python 3.13
* Django 5.2.8
* HTML5
* CSS3
* Bootstrap5 
* SQLite3 (padrão Django)

### Equipe Desenvolvedora

* Diego Alba
* Guilherme M. de Medeiros
* Lisandra Rosa de Vargas
* Lucas Sgarioni
* Luís Mendes

### 🌿 Sobre
Desenvolvido como parte de um projeto acadêmico e social com foco em sustentabilidade, cidadania e tecnologia acessível.

