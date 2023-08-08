from django.forms import ModelForm
from .models import Usuario
# from .models import FiltroMovientacao
from django import forms

# ProdutoForm
class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario # Produto
        fields = '__all__'

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='', widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'fileInput'}))


# ProdutoForm
# class ItemFilterMovimentacao(forms.Form):
    # txt_cod_produto = forms.CharField(max_length=50, required=False)
    # txt_nome_produto = forms.CharField(max_length=50, required=False)
    # txt_qtde_produto = forms.IntegerField(max_length=9999999999, required=False)