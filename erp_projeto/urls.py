
from django.urls import path
from app_cad_usuarios import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    # rota, view responsavel e nome de referencia

    # facebook.com
    path('', views.login, name='login'),
    # path('inicio/', views.home, name='home'),
    path('produtos/', views.produtos_teste, name='listagem_produtos'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('alterar/', views.alterar, name='alterar'),
    path('login/', views.login, name='login'),
    path('admin/', admin.site.urls),
]   