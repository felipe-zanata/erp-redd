import firebase_admin

from firebase_admin import credentials, firestore

class AuthUsuarios:
    def __init__(self) -> None:
        self.__dir_credencial = 'app_cad_usuarios\crud\credencial.json'
        self.__firebase = self.configura_credenciais()
        self.criar_colecao('admin')
        self.criar_colecao('geral')

    def configura_credenciais(self):
        """cria a conexao de autenticação"""
        try:
            cred = credentials.Certificate(self.__dir_credencial)
            firebase_admin.initialize_app(credential=cred)
            return firestore.client()
        
        except Exception as e:
            print("Erro ao configurar a autenticação", str(e))

    def criar_colecao(self, tipo: str):
        colecao = self.__firebase.collection('usuarios')
        documento_admin = colecao.document(tipo)
        documento_admin.set({})
        documento_admin.collection('id')

    def select_dados(self, nome_usuario: str, tipo_acesso: str):
        """retorna os dados dentro da coleção"""
        try:
            colecao = self.__firebase.collection('usuarios').document(tipo_acesso)
            colecao_id = colecao.collection('id')
            docs = colecao_id.get()

            for doc in docs:
                if doc['nome'] == nome_usuario:
                    return doc.to_dict()
            return {}

        except Exception as error:
            raise ValueError(error)

    def inserir_novo_usuario(self, dados: dict, tipo_usuario: str):
        """inseri um novo usuário na base de dados do Firebase"""
        try:
            colecao = self.__firebase.collection('usuarios')\
                                     .document(tipo_usuario)\
                                     .collection('id')
            
            id_do_usuario = colecao.add({**dados})    
        except Exception as erro:
            raise ValueError(erro)

if __name__ == '__main__':
    auth = AuthUsuarios()
    # auth.select_dados()


    # inserir novo usuario

    novo_usuario = {
        'nome': 'kz',
        'senha': '123',
        'avatar_url': 'http//teste',
        'email': 'luiz.cassimiro@gmail.com'
    }
    auth.inserir_novo_usuario(novo_usuario, 'geral')

