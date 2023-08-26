import datetime
import random
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
        try:
            self.__firebase.collection('estoque').add(dados)
            return "Produto registrado com sucesso"
        except Exception as e:
            return "Erro ao registrar o produto."

    def insert_novo_produto_massivo(self, json_data, request):

        # self.__firebase.collection('estoque').add(dados)
        batch = self.__firebase.batch()

        for item in json_data:
            dados = {
                'sku': item['sku'],
                'descricao': item['descricao'],
                'quantidade': item['quantidade'],
                'link': item['hiperlink'],
                'obs': item['obs']
            }
            # var = int(item['quantidade'])
            # if var > 0:
            #     self.baixa_produto(item['sku'], 
            #                        'entrada',
            #                        int(item['quantidade']), 
            #                        str(random.randint(8800,8899)), 
            #                        request.session.nome)
            
            # Crie uma referência para um novo documento na coleção
            novo_doc_ref = self.__firebase.collection('estoque').document()
            
            # Adicione os dados ao lote
            batch.set(novo_doc_ref, dados)
        
        # Commit do lote para inserir todos os documentos de uma vez
        batch.commit()

    def update_dados_produto(self, dados: dict):
        ret = self.select_dados_produto(dados['sku'])
        if ret:
            self.__firebase.collection('estoque').document(ret['id']).update(dados)

    def select_dados_produto(self, sku_id: str = None):
        
        dados = self.__firebase.collection('estoque').get()
        if sku_id:
            for doc in dados:
                dct_dados = doc.to_dict()
                if doc.id == sku_id:
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

        return data_hora_brasil.strftime('%d/%m/%y %H:%M')
    
    def baixa_produto(self, request, sku: str, tipo: str, qtde: int, referen: str, nome_usuario: str):

        produto = self.select_dados_produto(sku_id=sku)
        nova_qtde: int = 0
        if produto:
            # verifica tipo movimentação
            if tipo =='entrada':
                nova_qtde = int(produto["quantidade"]) + qtde
            else:
                nova_qtde = int(produto["quantidade"]) - qtde

            # altera os dados com a nova quantidade de estoque
            self.__firebase.collection('estoque').document(produto['id'])\
                                                 .update({'quantidade': nova_qtde})
            
            est = Movimentacao()
            dados = {
                'nome': nome_usuario,
                'data': self.data_fuso_horario(),
                'referencia': referen,
                'tipo': tipo.upper(),
                'sku':  produto['sku'],
                'descricao': produto['descricao'],
                'quantidade': qtde
            }
            est.insert_movimentacao(dados)
            # self.atualiza_produto(request, produto['id'], nova_qtde)

    def atualiza_produto(request, item_id: str, qtde: int):

        dct_produto: dict = request.session['dados_firebase']
        
        for chave, valor in dct_produto.items():
            if chave == item_id:
                dct_produto[item_id]['quantidade'] = qtde
                # import ipdb;ipdb.set_trace()
                break
        request.session['dados_firebase'] = dct_produto

#     def excluir_item_por_sku(sku):
#         collection_ref = firestore.client().collection('estoque')
#         docs = collection_ref.stream()

#         for doc in docs:
#             doc.reference.delete()
#             print(f"deletado: {sku}")
#         print("terminou")


# if __name__ == '__main__':
#     estoque = Estoque()
#     estoque.excluir_item_por_sku(sku="--")



    # import pandas as pd
    # # import random
    # estoque = Estoque()
    # # val = estoque.select_dados_produto()
    # # print(val)

    # df = pd.DataFrame(pd.read_excel(r"C:\Users\2103896595\Desktop\Pasta1.xlsx"))

    # for idx, row in df.iterrows():
    # dados = {
    #     'sku': '123abc',
    #     'descricao': 'teste',
    #     'quantidade': random.randint(1, 100),
    #     'url': 'https://www.google.com.br/',
    #     'obs': 'teste cadastro'
    # }

    
    # estoque.insert_novo_produto(dados)
    # update_dados = {
    #     'sku': '123abc',
    #     'url': 'http//url.arquivo.com',
    #     'obs': 'teste2',
    #     'quantidade': 16
    # }
    # estoque.update_dados_produto(update_dados)
    # estoque.delete_dados_produto('123abc')
