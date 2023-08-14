from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm
from .crud.firebase_crud import ProjetoEstoqueDemo
from .crud.firebase_auth import AuthUsuarios
from .crud.firebase_mov import Movimentacao
from .crud.firebase_est import Estoque
from .context_processors import nome_do_usuario 
from .forms import ExcelImportForm
import pandas as pd

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
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        auth = AuthUsuarios()
        data = auth.select_dados(email_usuario=email)
        if data['senha'] == senha:
            print("Logado!")
            request.session['id'] = data['id']
            request.session['tipo_acesso'] = data['tipo_acesso']
            request.session['senha'] = data['senha']
            request.session['nome'] = data['nome']
            request.session['avatar_url'] = data['avatar_url']
            request.session['email'] = data['email']
            return redirect('listagem_produtos')
        else:
            print("Senha incorreta")
        
    else:
        return render(request, 'login/login.html')

    return render(request, 'login/login.html')

def produtos_filtro(request):
    if request.method == 'GET':
        try:
            est = Estoque()
            dados = est.select_dados_produto()
            return render(request, 'produto/prodcadastrados.html', {'produtos': dados})
        
        except Exception as error:
            return render(request, 'produto/prodcadastrados.html')
    else:
        return render(request, 'produto/prodcadastrados.html')

def criar_user(request):
    if request.method == 'POST':
        nome = request.POST.get("nome")
        email = request.POST.get("email").lower().strip()
        senha1 = request.POST.get('password')
        acesso = request.POST.get('tipo')
        dados = {
            'nome' : nome,
            'email' : email,
            'senha' : senha1,
            'avatar_url': 'http//teste',
        }
        print(dados)
        new_user = AuthUsuarios()
        new_user.inserir_novo_usuario(dados=dados, tipo_usuario=acesso)
        
    return render(request, 'adm/criar_user.html')

def gerenciar(request):
    tipo_acesso = request.session.get('tipo_acesso', None)
    
    if tipo_acesso == "admin":
        return render(request, 'adm/gerenciar.html')
    else:
        return render(request, 'adm/sem_permissao.html')

def editar_user(request):
    if request.method == 'GET':
        try:
            auth = AuthUsuarios()
            dados = auth.select_dados()
            # print(dados)
            return render(request, 'adm/editar_remover_user.html', context={'dados': dados})
        except Exception as error:
            return render(request, 'adm/editar_remover_user.html')
    else:
        print("post")
        return render(request, 'adm/editar_remover_user.html')

def deletar_user(request):
    if request.method == 'GET':
        try:
            auth = AuthUsuarios()
            dados = auth.select_dados()
            # print(dados)
            return render(request, 'adm/editar_remover_user.html', context={'dados': dados})
        except Exception as error:
            return render(request, 'adm/editar_remover_user.html')
    else:
        print("post")
        return render(request, 'adm/editar_remover_user.html')

def movimentacao(request):
    if request.method == 'GET':
        try:
            mov = Movimentacao()
            dados = mov.select_movimentacao()
            return render(request, 'produto/movimentacao.html', context={'dados': dados})
            # return render(request, 'adm/editar_remover_user.html', context={'dados': dados})
        except Exception as error:
            return render(request, 'adm/editar_remover_user.html')
    else:
        print("post")
        return render(request, 'produto/movimentacao.html')
   
def dar_baixa(request, item_id):
    est = Estoque()
    dados = est.select_dados_produto(item_id)
    return render(request, 'produto/dar_baixa.html',{'dados': dados})

def importar_excel(request):
    if request.method == 'POST':
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            if excel_file.name.endswith('.xlsx'):
                excel_data = pd.read_excel(excel_file)

                excel_data.fillna("--", inplace=True)

                context = {
                    'excel_data': excel_data.to_dict(orient='records'),
                }

                return render(request, 'produto/importar_excel.html', context)
    else:
        form = ExcelImportForm()

    context = {'form': form}
    return render(request, 'produto/importar_excel.html', context)

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