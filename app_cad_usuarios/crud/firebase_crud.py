import random
import pyrebase
from decouple import config

class CadastroProduto:

    def __init__(self,sku: int, descricao: str, qtde: int = 0, preco: float = 0.0, obs: str = '') -> None:
        self.sku = sku
        self.descricao = descricao
        self.quantidade = qtde
        self.preco = preco
        self.obs = obs


class ProjetoEstoqueDemo:

    def __init__(self) -> None:
        self.__firebase_cofig = self.configuracao_firebase()
        # self.nivel_acesso = self.verifica_nivel()

    def configuracao_firebase(self):
        """insere os parametros de ligação"""
        try:
            firebase_config: dict = {
            'apiKey': config('API_KEY'),
            'authDomain':  config('AUTH_DOMAIN'),
            'databaseURL':  config('DATABASE_URL'),
            'projectId':  config('PROJECT_ID'),
            'storageBucket':  config('STORAGE_BUCKET'),
            'messagingSenderId': config('MESSAGING_SENDER_ID'),
            'appId':  config('APP_ID')
            }

            return pyrebase.initialize_app(firebase_config)
        except Exception as e:
            print("Erro ao configurar o Firebase", str(e))

    def inserir_produto(self, sku, descricao, quantidade, preco, obs):
        """cadastramento do novo produto na base"""
        try:
            cadastro_produto = CadastroProduto(sku, descricao, quantidade, preco, obs)
            db = self.__firebase_cofig.database()
            db.child('/produtos').child(cadastro_produto.sku).set({
                "Descricao" : cadastro_produto.descricao,
                "Quantidade": cadastro_produto.quantidade,
                "Preço": cadastro_produto.preco,
                "Obs": cadastro_produto.obs})
            print ("Novo registro adicionado com sucesso")

        except Exception as e:
            print("Erro ao cadastrar um produto no estoque", str(e))
    
    def inserir_historico_mov(self, sku, descricao, quantidade, preco, obs):
        """grava no banco de dados o historico de entrada e saida do produto"""
        try:
            cadastro_produto = CadastroProduto(sku, descricao, quantidade, preco, obs)
            db = self.__firebase_cofig.database()
            db.child('/movimentacao').child().set({
                "usuario" : cadastro_produto.descricao,
                "data": cadastro_produto.quantidade,
                "codigo": cadastro_produto.preco,
                "tipo": cadastro_produto.obs})
            print ("Novo registro adicionado com sucesso")

        except Exception as e:
            print("Erro ao cadastrar um produto no estoque", str(e))
    
    def alterar_qtde_produto(self, sku: int, new_qtde: int):
        """altera quantidade do produto"""
        try:
            db = self.__firebase_cofig.database()
            db.child('/produtos').child(sku).update({'Quantidade': new_qtde})
            print ('Qtde do produto {} atualizada para {}'.format(sku,new_qtde))
                                                                   
        except Exception as e:
            print("Erro ao atualizar a qtde do produto", str(e))

    def deletar_produto(self, sku):
        """remove sku da base"""
        try:
            db = self.__firebase_cofig.database()
            db.child("/produtos").child(sku).remove()
            print('Produto removido com Sucesso!')
        except Exception as e:
            print("Erro ao remover o produto", str(e))

    def listar_dados(self, codigo_filtro=None, nome_filtro=None, quantidade_filtro=None):
        """lista os dados da base com filtros opcionais"""
        try:
            db = self.__firebase_cofig.database()
            produtos = db.child("/produtos").get().val()  # Convertendo para um dicionário de produtos

            # Verificar se há algum filtro
            if not (codigo_filtro or nome_filtro or quantidade_filtro):
                return produtos  # Retorna todos os produtos se nenhum filtro foi especificado

            # Aplicar filtros se foram fornecidos
            produtos_filtrados = []
            for key, value in produtos.items():
                if (not codigo_filtro or key == codigo_filtro) and \
                (not nome_filtro or value.get('nome') == nome_filtro) and \
                (not quantidade_filtro or value.get('quantidade') == quantidade_filtro):
                    produtos_filtrados.append(value)

            return produtos_filtrados
        except Exception as e:
            print("Erro ao buscar os dados!", str(e))


if __name__ == '__main__':
    estoque = ProjetoEstoqueDemo()


    # INSERT
    # sku_fake = random.randint(10000, 99999) 
    # descricao = 'FRITADEIRA ELETRICA'
    # quantidade =  random.randint(1,10)
    # preco=random.uniform(10.,100.)
    # obs ='teste de cadastro'
    # estoque.inserir_produto(sku_fake, descricao, quantidade, preco, obs)
    # estoque.inserir_historico_mov(sku_fake, descricao, quantidade, preco, obs)

    # UPDATE
    # estoque.alterar_qtde_produto(sku=21412,new_qtde=10)

    # # DELETE
    # estoque.deletar_produto(sku=35678)

    # SELECT
# <<<<<<< stage_firebase
#     # estoque.listar_dados()

#     # SELECT
#     estoque.criar_novo_usuario()
# =======
#     estoque.listar_dados()
# >>>>>>> main
