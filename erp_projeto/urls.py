from django.urls import path
from app_cad_usuarios import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    # rota, view responsavel e nome de referencia

    # facebook.com
    path('', views.login, name='login'),
    # path('inicio/', views.home, name='home'),
    path('produtos/', views.produtos_filtro, name='listagem_produtos'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('deletar_produto/<int:sku>/', views.deletar, name='deletar_produto'),
    path('login/', views.login, name='login'),
    path('criar_user/', views.criar_user, name='criar_usuario'),
    path('adm/', views.gerenciar, name='gerenciar'),
    path('editar_user/', views.editar_user, name='editar_user'),
    path('admin/', admin.site.urls),
]   