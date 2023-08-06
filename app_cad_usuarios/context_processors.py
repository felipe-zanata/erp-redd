def nome_do_usuario(request):
    nome = None
    if request.method == "POST":
        nome = request.POST.get('nome')
        print(2,nome)
    return {'nome': nome}