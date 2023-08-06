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
            # cria uma numeração de sku fake

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

    def listar_dados(self):
        """lista todos os dados da base"""
        try:
            db = self.__firebase_cofig.database()
            produtos = db.child("/produtos").get()
            for item in produtos.each():
                print(item.key(), item.val(), sep=': ')
            
            return produtos
        except Exception as e:
            print("Erro ao buscar os dados!",str(e))
        


if __name__ == '__main__':
    estoque = ProjetoEstoqueDemo()


    # INSERT
    sku_fake = random.randint(10000, 99999) 
    descricao = 'FRITADEIRA ELETRICA'
    quantidade =  random.randint(1,10)
    preco=random.uniform(10.,100.)
    obs ='teste de cadastro'
    estoque.inserir_produto(sku_fake, descricao, quantidade, preco, obs)

    # UPDATE
    estoque.alterar_qtde_produto(sku=21412,new_qtde=10)

    # DELETE
    estoque.deletar_produto(sku=35678)

    # SELECT
    estoque.listar_dados()