from django.db import models
# Produto
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    codigo_produto = models.TextField()
    nome_produto = models.TextField()
    qtidade_produto = models.IntegerField()
    obs_produto = models.TextField()

# class FiltroMovientacao(models.Model):
#     txt_cod_produto = models.CharField(max_length=50)
#     txt_nome_produto = models.CharField(max_length=50)
#     txt_qtde_produto = models.IntegerField(max_length=50)