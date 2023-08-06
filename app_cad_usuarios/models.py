from django.db import models
# Produto
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    codigo_produto = models.TextField()
    nome_produto = models.TextField()
    qtidade_produto = models.IntegerField()
    obs_produto = models.TextField()