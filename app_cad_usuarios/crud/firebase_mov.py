from datetime import date, datetime
import firebase_admin

from firebase_admin import credentials, firestore

class Movimentacao:

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
        colecao = self.__firebase.collection('movimentacao').add({})

    def insert_movimentacao(self, dados: dict):
        self.__firebase.collection('movimentacao').add(dados)

    def update_movimentacao(self, dados: dict):
        ret = self.select_movimentacao(dados['sku'])
        if ret:
            self.__firebase.collection('movimentacao').document(ret['id']).update(dados)

    def select_movimentacao(self, sku: str = None):
        
        dados = self.__firebase.collection('movimentacao').get()
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

    def delete_movimentacao(self, sku: str):
        dados = self.select_movimentacao(sku)
        if dados:
            self.__firebase.collection('movimentacao').document(dados['id']).delete()


if __name__ == '__main__':
    estoque = Movimentacao()
    # estoque.consultar_dados_produto()

    dados = {
        'nome': 'luiz',
        'data': datetime.now(),
        'referencia': '8806',
        'tipo': 'SAIDA',
        'sku': 'fritadeira',
        'quantidade': 10
    }
    estoque.insert_movimentacao(dados)
    update_dados = {

    }
    # estoque.update_dados_produto(update_dados)
    # estoque.delete_dados_produto('123abc')

# import datetime
# import pytz

# # Defina o fuso horário do Brasil (America/Sao_Paulo ou America/Rio_Branco, por exemplo)
# fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

# # Obtenha a data e hora atual no fuso horário UTC
# data_hora_utc = datetime.datetime.utcnow()

# # Adicione o fuso horário do Brasil à data e hora atual
# data_hora_brasil = data_hora_utc.replace(tzinfo=pytz.utc).astimezone(fuso_horario_brasil)

# # Imprima a data e hora no fuso horário do Brasil
# print("Data e hora no Brasil:", data_hora_brasil.strftime('%Y-%m-%d %H:%M:%S %Z'))