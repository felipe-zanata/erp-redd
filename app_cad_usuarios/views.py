from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm
from .crud.firebase_crud import ProjetoEstoqueDemo
from .context_processors import nome_do_usuario 

# def home(request):
#     return render(request, 'base/home.html')

import json
from django.http import JsonResponse

def cadastrar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sku = data.get('sku')
            descricao = data.get('descricao')
            quantidade = data.get('quantidade')
            preco = data.get('preco')
            obs = data.get('obs')
            projeto = ProjetoEstoqueDemo()
            projeto.inserir_produto(sku, descricao, quantidade, preco, obs)

            return redirect('listagem_produtos')

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    else:
        usuario_form = UsuarioForm()
        produtos = {'formulario': usuario_form}
        return render(request, 'produto/cadastro.html', context=produtos)

def alterar(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario_form.save()
        return redirect('listagem_produtos')
    else:
        usuario_form = UsuarioForm()
        produtos = {'formulario': usuario_form}
        return render(request, 'produto/alterar.html', context=produtos)

def deletar(request, sku):
    pass

def login(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        if nome:
            request.session['nome_usuario'] = nome
            nome_session = request.session.get('nome_usuario', 'Usuário Anônimo')
            projeto = ProjetoEstoqueDemo()
            dados_filtrados = projeto.listar_dados()
        return redirect('listagem_produtos')
    else:
        return render(request, 'login/login.html')

def produtos_filtro(request):
    nome = nome_do_usuario(request)['nome']
    projeto = ProjetoEstoqueDemo()
    # Recuperar os parâmetros de filtro do request.GET
    codigo_filtro = request.GET.get('codigo_filtro')
    nome_filtro = request.GET.get('nome_filtro')
    quantidade_filtro = request.GET.get('quantidade_filtro')

    # Chamar a função listar_dados com os parâmetros de filtro
    dados_filtrados = projeto.listar_dados(codigo_filtro, nome_filtro, quantidade_filtro)

    # Passar os dados filtrados para o template
    return render(request, 'produto/prodcadastrados.html', {'produtos': dados_filtrados, 'nome': nome})

def criar_user(request):
    return render(request, 'adm/criar_user.html')

def gerenciar(request):
    return render(request, 'adm/gerenciar.html')

def editar_user(request):
    return render(request, 'adm/editar_remover_user.html')

def movimentacao(request):
    return render(request, 'produto/movimentacao.html')

def dar_baixa(request):
    return render(request, 'produto/dar_baixa.html')

# def login(request):
#     # Verificação de usuário e senha pré-definidos
#     usuario_predefinido = 'geoteste'
#     senha_predefinida = 'geo'
    
#     if request.method == 'POST':
#         usuario_digitado = request.POST.get('usuario')
#         senha_digitada = request.POST.get('senha')
        
#         if usuario_digitado == usuario_predefinido and senha_digitada == senha_predefinida:
#             return redirect('inicio')  # Redireciona para a página de início
#         else:
#             # Código para exibir mensagem de erro de login
#             pass
            
#     return render(request, 'usuarios/login.html')