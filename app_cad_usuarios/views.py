import random
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
from firebase_admin import auth


# def home(request):
#     return render(request, 'base/home.html')

import json
from django.http import JsonResponse

def cadastrar(request):
    if request.method == 'POST':
        try:
            # data = json.loads(request.body)
            # print(data)
            dados = {
                'sku': request.POST.get('sku'),
                'descricao': request.POST.get('descricao'),
                'quantidade': request.POST.get('quantidade'),
                'link': request.POST.get('hiperlink'),
                'obs': request.POST.get('obs')
            }

            projeto = Estoque()
            projeto.insert_novo_produto(dados)

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
    try: 
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
                return render(request, 'login/login_erro.html', {'error_message': 'Usuário ou senha incorretos'})
            
        else:
            return render(request, 'login/login.html')
    except:
        return render(request, 'login/login_erro.html', {'error_message': 'Usuário ou senha incorretos'})

def produtos_filtro(request):
    if request.method == 'GET':
        try:
            if 'dados_firebase' not in request.session:
                est = Estoque()
                dados = est.select_dados_produto()
                request.session['dados_firebase'] = dados
            return render(request, 'produto/prodcadastrados.html', {'produtos': request.session['dados_firebase']})
        
        except Exception as error:
            return render(request, 'produto/prodcadastrados.html')
    else:
        return render(request, 'produto/prodcadastrados.html')

def atualizar_dados(request):
    try:
        if 'dados_firebase' in request.session:
            del request.session['dados_firebase']
        
        est = Estoque()
        dados = est.select_dados_produto()
        request.session['dados_firebase'] = dados

        return render(request, 'produto/produtos_list.html', {'produtos': dados})

    except Exception as error:
        return render(request, 'produto/produtos_list.html')

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
    return render(request, 'adm/editar_user.html')

def gerenciar_user(request):
    if request.method == 'GET':
        try:
            auth = AuthUsuarios()
            dados = auth.select_dados()
            # print(dados)
            return render(request, 'adm/gerenciar_user.html', context={'dados': dados})
        except Exception as error:
            return render(request, 'adm/gerenciar_user.html')
    else:
        print("post")
        return render(request, 'adm/gerenciar_user.html')

def deletar_user(request):
    if request.method == 'GET':
        try:
            auth = AuthUsuarios()
            dados = auth.select_dados()
            # print(dados)
            return render(request, 'adm/gerenciar_user.html', context={'dados': dados})
        except Exception as error:
            return render(request, 'adm/gerenciar_user.html')
    else:
        print("post")
        return render(request, 'adm/gerenciar_user.html')

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
    # est = Estoque()
    # dados = est.select_dados_produto(item_id)
    # dados['item_id'] = item_id
    dados = {

        "item_id": item_id,
        "sku": request.GET.get('sku'),
        "descricao" : request.GET.get('desc'),
        'quantidade' : request.GET.get('qtde')

    }
    return render(request, 'produto/dar_baixa.html',{'dados': dados})

def exec_baixa(request):
    if request.method == 'POST':
        operador = request.POST.get('operador')
        id_registro = request.POST.get('id_registro')
        tipo = request.POST.get('tipo')
        qtidade_produto_baixa = int(request.POST.get('qtidade-produto-baixa'))
        baixa = Estoque()
        baixa.baixa_produto(
                            request=request,
                            sku=id_registro, 
                            tipo=tipo, 
                            qtde=qtidade_produto_baixa,
                            referen=str(random.randint(8800, 8899)), 
                            nome_usuario=operador)
        
    return redirect('listagem_produtos')

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

# def carregar_dados_excel(request):
#     import pandas as pd
#     estoque = Estoque()

#     df = pd.DataFrame(pd.read_excel(''))

#     for idx, row in df.iterrows():
#         if not row['sku'] == '--':
#             dados = {
#                 'sku': row['sku'],
#                 'descricao': str(row['Descricao']),
#                 'quantidade': 0,
#                 'url': row['url'],
#                 'obs': row['obs']
#             }
#             estoque.insert_novo_produto(dados)
#     return render(request, 'produto/importar_excel.html')

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

def logout(request):
    # Lógica para o logout (remova o usuário da sessão e outras ações necessárias)
    request.session.flush()  # Isso limpa todas as informações da sessão
    
    return redirect('login')  # Redirecione para a página de login após o logout