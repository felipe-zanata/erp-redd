from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm
from .firebase_crud import ProjetoEstoqueDemo

# def home(request):
#     return render(request, 'usuarios/home.html')

def cadastrar(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario_form.save()
        return redirect('listagem_produtos')
    else:
        usuario_form = UsuarioForm()
        produtos = {'formulario': usuario_form}
        return render(request, 'usuarios/cadastro.html', context=produtos)

def alterar(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        if usuario_form.is_valid():
            usuario_form.save()
        return redirect('listagem_produtos')
    else:
        usuario_form = UsuarioForm()
        produtos = {'formulario': usuario_form}
        return render(request, 'usuarios/alterar.html', context=produtos)

def login(request):
    return render(request, 'usuarios/login.html')

# def login(request):
#     # Verificação de usuário e senha pré-definidos
#     usuario_predefinido = 'teste'
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

def usuarios(request):
    # Salvar dados da tela para o DB
    if request.method == 'POST':
        novo_usuario = UsuarioForm()
        novo_usuario.produto = request.POST.get('codprod')
        novo_usuario.nome = request.POST.get('nomeprod')
        novo_usuario.qtidade = request.POST.get('qtdprod')
        novo_usuario.obs = request.POST.get('obsprod')
        novo_usuario.save()
        return redirect('listagem_produtos')
    else:
        usu_form = UsuarioForm()
        # Exibir produtos cadastrados em uma nova página
        usuarios = {
            'usuario': usu_form
        }
        # Retornar dados para página de produtos cadastrados
        return render(request, 'usuarios/prodcadastrados.html', context=usuarios)
    
def produtos_teste(request):
    projeto = ProjetoEstoqueDemo()
    produtos_data = projeto.listar_dados()

    # codigo = produtos_data.key()
    # descricao = produtos_data.child('descricao').val()
    # quantidade = produtos_data.child('quantidade').val()
    # obs = produtos_data.child('obs').val()

    produtos = {
        'produtos': produtos_data.val()
    }
    # produtos = {'produtos': Usuario.objects.all()}
    return render(request, 'usuarios/prodcadastrados.html', context=produtos)