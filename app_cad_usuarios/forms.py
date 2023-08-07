from django.forms import ModelForm
from .models import Usuario
from django import forms

# ProdutoForm
class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario # Produto
        fields = '__all__'

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='')