import firebase_admin

from firebase_admin import credentials, firestore

class Estoque:

    def __init__(self) -> None:
        self.__dir_credencial = 'app_cad_usuarios\crud\credencial.json'
        self.__firebase = self.configura_credenciais()
        # self.criar_colecao()

    def configura_credenciais(self):
        """cria a conexao de autenticação"""
        try:
            cred = credentials.Certificate(self.__dir_credencial)
            firebase_admin.initialize_app(credential=cred)
            return firestore.client()
        
        except Exception as e:
            print("Erro ao configurar a autenticação", str(e))

    def criar_colecao(self):
        colecao = self.__firebase.collection('estoque').add({})

    def insert_novo_produto(self, dados: dict):
        self.__firebase.collection('estoque').add(dados)

    def update_dados_produto(self, dados: dict):
        ret = self.select_dados_produto(dados['sku'])
        if ret:
            self.__firebase.collection('estoque').document(ret['id']).update(dados)

    def select_dados_produto(self, sku: str = None):
        
        dados = self.__firebase.collection('estoque').get()
        if sku:
            for doc in dados:
                dct_dados = doc.to_dict()
                if dct_dados['sku'] == sku:
                    return {'id':doc.id, **dct_dados}
            return {}
        else:
            lista_produtos = {}
            for doc in dados:
                lista_produtos[doc.id] = dados.to_dict()
            return lista_produtos

    def delete_dados_produto(self, sku: str):
        dados = self.select_dados_produto(sku)
        if dados:
            self.__firebase.collection('estoque').document(dados['id']).delete()


if __name__ == '__main__':
    estoque = Estoque()
    # estoque.consultar_dados_produto()

    # dados = {
    #     'sku': '123abc',
    #     'descricao': 'FRITADEIRA ELETRICA',
    #     'quantidade': 1,
    #     'url': 'http//url.arquivo.com',
    #     'obs': 'teste cadastro'
    # }
    # estoque.insert_novo_produto(dados)
    update_dados = {
        'sku': '123abc',
        'url': 'http//url.arquivo.com',
        'obs': 'teste2',
        'quantidade': 16
    }
    estoque.update_dados_produto(update_dados)
    # estoque.delete_dados_produto('123abc')
