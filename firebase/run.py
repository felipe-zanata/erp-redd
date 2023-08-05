from src.firebase_crud import ProjetoEstoqueDemo
import os
import time


while True:
    os.system('cls')
    print("1 - Cadastrar produto")
    print("2 - Listar todos os produtos cadastrados no estoque de umprojeto específico.")
    print("3 - Atualizar dados do produto")
    print("4 - Excluir produto")
    print("5 - Sair")

    opcao = input('Digite a opção: ')
    match opcao:
        case '1':
            nomeProduto=input('Digite o sku do produto:')
            descricaoDoProduto=input('Digite uma descrição para o produto: ')
            precoUnitario=float(input('Digite o valor unitário do produto: '))
            quantidadeEmEstoque=int(input('Digite a quantidade em estoque deseja adicionar ao produto:' ))
            obs = str(input('Digite obs Adicionais: '))
            estoque = ProjetoEstoqueDemo()
            estoque.inserir_produto(nomeProduto, descricaoDoProduto, quantidadeEmEstoque,precoUnitario, obs)
        case '2':
            estoque = ProjetoEstoqueDemo()
            estoque.listar_dados()
            sair = input('Tecla "enter" para voltar ao menu principal')
        case '3':
            estoque = ProjetoEstoqueDemo()
            nomeProduto=input('Digite o sku do produto:')
            quantidadeEmEstoque=int(input('Digite a quantidade em estoque deseja altererar ao produto:' ))
            estoque.alterar_qtde_produto(sku=nomeProduto,new_qtde=quantidadeEmEstoque)
        case "4":
            nomeProduto=int(input('Digite o sku do produto: '))
            estoque = ProjetoEstoqueDemo()
            estoque.deletar_produto(sku=nomeProduto)
        case '5':
            break
        case _:
            print("Opção inválida!")
        
    time.sleep(3)
                                        
