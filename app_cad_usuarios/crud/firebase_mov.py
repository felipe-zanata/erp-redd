import datetime
import firebase_admin
import pytz

from firebase_admin import credentials, firestore

class Movimentacao:
    _instance = None
    def __init__(self) -> None:
        self.__dir_credencial = 'app_cad_usuarios\crud\credencial.json'
        self.__firebase = self.configura_credenciais()
        # self.criar_colecao()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Movimentacao, cls).__new__(cls)
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
        colecao = self.__firebase.collection('movimentacao').add({})

    def insert_movimentacao(self, dados: dict):
        self.__firebase.collection('movimentacao').add(dados)

    def update_movimentacao(self, dados: dict):
        ret = self.select_movimentacao(dados['sku'])
        if ret:
            self.__firebase.collection('movimentacao').document(ret['id']).update(dados)

    def select_movimentacao(self):
        dados = self.__firebase.collection('movimentacao').get()
        dct_mov = {doc.id: doc.to_dict() for doc in dados}

        dados_ordenados = dict(sorted(dct_mov.items(), key=lambda item: item[1]['data'], reverse=True))
        return dados_ordenados

    def delete_movimentacao(self, sku: str):
        dados = self.select_movimentacao(sku)
        if dados:
            self.__firebase.collection('movimentacao').document(dados['id']).delete()

        
if __name__ == '__main__':

    def data_fuso_horario():
        # Defina o fuso horário do Brasil (America/Sao_Paulo ou America/Rio_Branco, por exemplo)
        fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')

        # Obtenha a data e hora atual no fuso horário UTC
        data_hora_utc = datetime.datetime.utcnow()

        # Adicione o fuso horário do Brasil à data e hora atual
        data_hora_brasil = data_hora_utc.replace(tzinfo=pytz.utc).astimezone(fuso_horario_brasil)

        return data_hora_brasil.strftime('%d/%m/%y %H:%M')
    
    estoque = Movimentacao()
    # estoque.consultar_dados_produto()

    # # INSERT
    # dados = {
    #     'nome': 'luiz',
    #     'data': data_fuso_horario(),
    #     'referencia': '8807',
    #     'tipo': 'ENTRADA',
    #     'sku': 'DP08',
    #     'descricao': 'GELADEIRA',
    #     'quantidade': 200
    # }
    # estoque.insert_movimentacao(dados)

    # # UPDATE
    # update_dados = {
    #     'nome': 'luiz',
    #     'data': data_fuso_horario(),
    #     'referencia': '8806',
    #     'tipo': 'SAIDA',
    #     'sku': 'CM07',
    #     'descricao': 'fritadeira',
    #     'quantidade': 2000
    # }
    
    # # DELETE
    # estoque.delete_movimentacao(update_dados)

    # SELECT
    val = estoque.select_movimentacao()
    print(val)



