from django.forms import ModelForm
from .models import Usuario
# ProdutoForm
class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario # Produto
        fields = '__all__'