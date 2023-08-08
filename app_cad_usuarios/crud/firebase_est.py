import datetime
import firebase_admin

from firebase_admin import credentials, firestore
import pytz
from firebase_mov import Movimentacao

class Estoque:
    _instance = None

    def __init__(self) -> None:
        self.__dir_credencial = 'app_cad_usuarios\crud\credencial.json'
        self.__firebase = self.configura_credenciais()
        # self.criar_colecao()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Estoque, cls).__new__(cls)
        return cls._instance

    def configura_credenciais(self):
        """cria a conexao de autenticação"""
        try:
            if not firebase_admin._apps:
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
            lista_produtos: dict = {doc.id: doc.to_dict() for doc in dados}
            return lista_produtos

    def delete_dados_produto(self, sku: str):
        dados = self.select_dados_produto(sku)
        if dados:
            self.__firebase.collection('estoque').document(dados['id']).delete()

    def data_fuso_horario(self):
        # Defina o fuso horário do Brasil (America/Sao_Paulo ou America/Rio_Branco, por exemplo)
        fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

        # Obtenha a data e hora atual no fuso horário UTC
        data_hora_utc = datetime.datetime.utcnow()

        # Adicione o fuso horário do Brasil à data e hora atual
        data_hora_brasil = data_hora_utc.replace(tzinfo=pytz.utc).astimezone(fuso_horario_brasil)

        return data_hora_brasil
    
    def baixa_produto(self, sku: str, tipo: str, qtde: int, referen: str, nome_usuario: str):

        produto = self.select_dados_produto(sku=sku)
        if produto:
            # verifica tipo movimentação
            if tipo =='entrada':
                nova_qtde = produto["quantidade"] + qtde
            else:
                nova_qtde = produto["quantidade"] - qtde

            self.__firebase.collection('estoque').document(produto['id'])\
                                                 .update({'quantidade': nova_qtde})
            
            est = Movimentacao()
            dados = {
                'nome': nome_usuario,
                'data': self.data_fuso_horario(),
                'referencia': referen,
                'tipo': tipo,
                'sku':  produto['sku'],
                'descricao': produto['descricao'],
                'quantidade': qtde
            }
            est.insert_movimentacao(dados)

            




if __name__ == '__main__':
    estoque = Estoque()
    # estoque.consultar_dados_produto()

    dados = {
        'sku': '123abc',
        'descricao': 'FRITADEIRA ELETRICA',
        'quantidade': 1,
        'url': 'http//url.arquivo.com',
        'obs': 'teste cadastro'
    }
    estoque.insert_novo_produto(dados)
    # update_dados = {
    #     'sku': '123abc',
    #     'url': 'http//url.arquivo.com',
    #     'obs': 'teste2',
    #     'quantidade': 16
    # }
    # estoque.update_dados_produto(update_dados)
    # estoque.delete_dados_produto('123abc')
