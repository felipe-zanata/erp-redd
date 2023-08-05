# import pyrebase
# import urllib3


# firebase= pyrebase.initialize_app(firebase_config)
# autenticacao = firebase.auth()

# def cadastro_usuario():
#     """cria um novo usuario dentro do firebase"""
#     try:
#         print("CASDASTRO DE USUARIO", "#" * 30)
#         email = str(input("Novo Email: "))
#         print("#"*30)
#         senha = str(input("Nova Senha: "))
#         print("#"*30)

#         user = autenticacao.create_user_with_email_and_password(email=email,password=senha)
#     except Exception as e:
#         print('Erro ao cadastrar usuário',str(e))

# def login_usuario():
#     """realiza o login od usario no firebase"""
#     try:
#         print("ACESSO DE USUARIO", "#" * 30)
#         email = str(input("Email: "))
#         print("#"*30)
#         senha = str(input("Senha: "))
#         print("#"*30)
#     except Exception as e:
#         print('Verifique Usuario e Senha')


# opc = str(input('Usuario ja possui cadastro? [y/n]: '))

# if opc.lower() in 'Yy':
#     login_usuario()
# elif opc.lower() in 'Nn':
#     cadastro_usuario()