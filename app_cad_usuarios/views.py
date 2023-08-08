from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm
from .crud.firebase_crud import ProjetoEstoqueDemo
from .crud.firebase_auth import AuthUsuarios
from .crud.firebase_mov import Movimentacao
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
    projeto = ProjetoEstoqueDemo()
    # Recuperar os parâmetros de filtro do request.GET
    codigo_filtro = request.GET.get('codigo_filtro')
    nome_filtro = request.GET.get('nome_filtro')
    quantidade_filtro = request.GET.get('quantidade_filtro')

    # Chamar a função listar_dados com os parâmetros de filtro
    dados_filtrados = projeto.listar_dados(codigo_filtro, nome_filtro, quantidade_filtro)

    # Passar os dados filtrados para o template
    return render(request, 'produto/prodcadastrados.html', {'produtos': dados_filtrados})

def criar_user(request):
    return render(request, 'adm/criar_user.html')

def gerenciar(request):
    return render(request, 'adm/gerenciar.html')

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
            print(dados)
            return render(request, 'produto/movimentacao.html', context={'dados': dados})
            # return render(request, 'adm/editar_remover_user.html', context={'dados': dados})
        except Exception as error:
            return render(request, 'adm/editar_remover_user.html')
    else:
        print("post")
        return render(request, 'produto/movimentacao.html')
    
# def filter_movimentacao(request):
#     item = FiltroMovientacao.objects.all()
#     item_filtrado = None

#     if request.method == 'GET':
#         filtro = ItemFilterMovimentacao(request.GET)
#         if filtro.is_valid():
#             dados_filtro = filtro.cleaned_data
#             item_filtrado = item

#             if dados_filtro['txt_cod_produto']:
#                 item_filtrado = item_filtrado.filter(txt_cod_produto__icontains=dados_filtro['txt_cod_produto'])

#             if dados_filtro['txt_nome_produto']:
#                 item_filtrado = item_filtrado.filter(txt_nome_produto__icontains=dados_filtro['txt_nome_produto'])

#             if dados_filtro['txt_qtde_produto']:
#                 item_filtrado = item_filtrado.filter(txt_qtde_produto__icontains=dados_filtro['txt_qtde_produto'])
#         else:
#             filtro = ItemFilterMovimentacao()

#         context = {
#             'filtro': filtro,
#             'item_filtrado': item_filtrado

#         }

#         return render(request, 'produto/movimentacao.html', context=context)
    
def dar_baixa(request):
    return render(request, 'produto/dar_baixa.html')

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