from django.urls import path
from app_cad_usuarios import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    # rota, view responsavel e nome de referencia

    # facebook.com
    path('', views.login, name='login'),
    # path('inicio/', views.home, name='home'),
    path('produtos_redd/', views.tela_produtos, name='tela_produtos'),
    path('produtos/', views.produtos_filtro, name='listagem_produtos'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('login/', views.login, name='login'),
    path('criar_user/', views.criar_user, name='criar_usuario'),
    path('gerenciar_user/', views.gerenciar_user, name='gerenciar_user'),
    path('gerenciar_user/<str:user_id>/', views.gerenciar_user, name='gerenciar_user'),
    path('deletar_user/<str:user_id>/', views.deletar_user, name='deletar_user'),
    path('adm/', views.gerenciar, name='gerenciar'),
    path('movimentacao/', views.movimentacao, name='movimentacao'),
    path('dar_baixa/<str:item_id>/', views.dar_baixa, name='baixa'),
    path('exec_baixa/', views.exec_baixa, name='exe_baixa'),
    path('importar_excel/', views.importar_excel, name='importar_excel'),
    path('carregar_dados_excel/', views.carregar_dados_excel, name='carregar_dados_excel'),
    path('login_incorreto/', views.login, name='login_erro'),
    path('logout/', views.logout, name='logout'),
    path('editar_user/', views.editar_user, name='editar_user'),
    # path('admin/', admin.site.urls),
]   