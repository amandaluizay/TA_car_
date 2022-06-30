from django.shortcuts import redirect, render
from core.forms import *
from core.models import *
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# Create your views here.


def home(request):
    return render(request, './index.html')


class Registrar(generic.CreateView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = 'registration/register.html'


# Cliente
def cadastro_cliente(request):
    try:
        form = FormCliente(request.POST or None, request.FILES or None)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            form.save()
            messages.success(request, f'Cliente {nome} cadastrado com sucesso!')
            return redirect('url_lista_clientes')
        contexto = {'form': form, 'titulo': 'Cadastro de cliente', 'stringBotao': 'Cadastrar'}
        return render(request, 'core/cadastro.html', contexto)
    except Exception as mensagem_erro:
        contexto = {'msg_erro': mensagem_erro}
        return render(request, '500.html', contexto)


def lista_cliente(request):
    dados = Cliente.objects.all()
    if request.POST:
        if request.POST['pesquisa']:
            dados = Cliente.objects.filter(nome=request.POST['pesquisa'])

    contexto = {'dados': dados}
    return render(request, 'core/lista_cliente.html', contexto)


def altera_cliente(request, id):
    objeto = Cliente.objects.get(id=id)
    form = FormCliente(request.POST or None, request.FILES or None, instance=objeto)

    if form.is_valid():
        nome = form.cleaned_data['nome']
        form.save()
        messages.success(request, f'Dados do cliente {nome} atualizados com sucesso!')
        return redirect('url_lista_clientes')

    contexto = {'form': form, 'titulo': 'Atualização de clientes', 'stringBotao': 'Atualizar'}
    return render(request, 'core/cadastro.html', contexto)


def exclui_cliente(request, id):
    objeto = Cliente.objects.get(id=id)
    if request.POST:
        objeto.delete()
        return redirect('url_lista_clientes')
    contexto = {'url': '/lista_clientes', 'objeto': objeto.nome}
    return render(request, 'core/mensagem_excluir.html', contexto)


# Veiculos
def cadastro_veiculo(request):
    form = FormVeiculo(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'titulo': 'Cadastro de veículos', 'stringBotao': 'Cadastrar'}
    return render(request, 'core/cadastro.html', contexto)


def lista_veiculo(request):
    dados = Veiculo.objects.all()
    if request.POST:
        if request.POST['pesquisa']:
            dados = Veiculo.objects.filter(placa=request.POST['pesquisa'])
    contexto = {'dados': dados}
    return render(request, 'core/lista_veiculo.html', contexto)


def altera_veiculo(request, id):
    objeto = Veiculo.objects.get(id=id)
    form = FormVeiculo(request.POST or None, request.FILES or None, instance=objeto)

    if form.is_valid():
        form.save()
        contexto = {'objeto': objeto.modelo, 'url': '/lista_veiculos/', 'titulo': 'Atualização de veículos',
                    'stringBotao': 'Atualizar'}
        return render(request, 'core/mensagem_salva.html', contexto)

    contexto = {'form': form, 'titulo': 'Atualização de veículos', 'stringBotao': 'Atualizar'}
    return render(request, 'core/cadastro.html', contexto)


def exclui_veiculo(request, id):
    objeto = Veiculo.objects.get(id=id)
    if request.POST:
        objeto.delete()
        return redirect('url_lista_veiculos')
    contexto = {'url': '/lista_veiculos', 'objeto': objeto.modelo}
    return render(request, 'core/mensagem_excluir.html', contexto)


# Fabricante
def cadastro_fabricante(request):
    form = FormFabricante(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'titulo': 'Cadastro de fabricantes', 'stringBotao': 'Cadastrar'}
    return render(request, 'core/cadastro.html', contexto)


def lista_fabricantes(request):
    dados = Fabricante.objects.all()
    if request.POST:
        if request.POST['pesquisa']:
            dados = Fabricante.objects.filter(descricao=request.POST['pesquisa'])
    contexto = {'dados': dados}
    return render(request, 'core/lista_fabricantes.html', contexto)


# Preços

def cadastro_preco(request):
    form = FormPreco(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_tabela_preco')
    contexto = {'form': form, 'Descrição': 'Valor', 'stringBotao': 'Cadastrar'}
    return render(request, 'core/cadastro.html', contexto)


def cadastro_pagamento(request):
    form = FormPagamento(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_principal')
    contexto = {'form': form, 'título': 'Cadastro Forma de pagamento ', 'stringBotao': 'Cadastrar'}
    return render(request, 'core/cadastro.html', contexto)

def tabela_preco(request):
    dados = Preco.objects.all()
    contexto = {'dados': dados}
    return render(request, 'core/tabela_preco.html', contexto)


# Rotativo
def cadastro_rotativo(request):
    form = FormCadastroRotativo(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_lista_rotativo')
    contexto = {'form': form, 'titulo': 'Cadastro de rotativo', 'stringBotao': 'Cadastrar', 'calendario': True}
    return render(request, 'core/cadastro.html', contexto)


def listagem_rotativo(request):
    dados = Rotativo.objects.all()
    if request.POST:
        if request.POST['pesquisa']:
            dados = Rotativo.objects.filter(veiculo=request.POST['pesquisa'])
    contexto = {'dados': dados}
    return render(request, 'core/lista_rotativo.html', contexto)


def altera_rotativo(request, id):
    objeto = Rotativo.objects.get(id=id)
    form = FormRotativo(request.POST or None, request.FILES or None, instance=objeto)

    if form.is_valid():
        objeto.calcula_total()
        form.save()
        return redirect('url_lista_rotativo')

    contexto = {'form': form, 'titulo': 'Atualização de rotativo', 'stringBotao': 'Atualizar'}
    return render(request, 'core/cadastro.html', contexto)


# Mensalista


def cadastro_mensalista(request):
    form = FormMensalista(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('url_lista_mensalista')
    contexto = {'form': form, 'titulo': 'Cadastro de mensalista', 'stringBotao': 'Cadastrar'}
    return render(request, 'core/cadastro.html', contexto)


def listagem_mensalista(request):
    dados = Mensalista.objects.all()
    contexto = {'dados': dados}
    return render(request, 'core/lista_mensalista.html', contexto)


def altera_mensalista(request, id):
    objeto = Mensalista.objects.get(id=id)
    form = FormMensalista(request.POST or None, request.FILES or None, instance=objeto)

    if form.is_valid():
        form.save()
        context = {'objeto': objeto.id_cliente, 'url': '/lista_mensalista/', 'titulo': 'Atualização de mensalistas',
                   'stringBotao': 'Atualizar'}
        return render(request, 'core/mensagem_salva.html', context)

    contexto = {'form': form, 'titulo': 'Atualização de mensalistas', 'stringBotao': 'Atualizar'}
    return render(request, 'core/cadastro.html', contexto)


def exclui_mensalista(request, id):
    objeto = Mensalista.objects.get(id=id)
    if request.POST:
        objeto.delete()
        return redirect('url_lista_mensalista')
    contexto = {'url': '/lista_mensalista', 'objeto': objeto.id_cliente}
    return render(request, 'core/mensagem_excluir.html', contexto)
