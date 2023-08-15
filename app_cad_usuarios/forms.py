from django import forms


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='', widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'fileInput'}))

