from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registrar/', Registrar.as_view(), name="url_registrar"),
    path('', home, name='url_principal'),

    #Clientes
    path('cadastro_cliente/', cadastro_cliente),
    path('lista_clientes/', lista_cliente, name="url_lista_clientes"),
    path('altera_cliente/<int:id>/', altera_cliente, name="url_altera_cliente"),
    path('exclui_cliente/<int:id>/', exclui_cliente, name="url_exclui_cliente"),

    #Veiculos
    path('cadastro_veiculos/', cadastro_veiculo),
    path('lista_veiculos/', lista_veiculo, name="url_lista_veiculos"),
    path('altera_veiculo/<int:id>/', altera_veiculo, name="url_altera_veiculo"),
    path('exclui_veiculo/<int:id>/', exclui_veiculo, name="url_exclui_veiculo"),

    #Fabricantes
    path('cadastro_fabricantes/', cadastro_fabricante),
    path('lista_fabricantes/', lista_fabricante),

    #Tabela de preços
    path('tabela/', tabela_preco),

    #Rotativo
    path('cadastro_rotativo/', cadastro_rotativo, name="url_cadstro_rotativo"),
    path('lista_rotativo/', listagem_rotativo, name="url_lista_rotativo"),
    path('altera_rotativo/<int:id>/', altera_rotativo, name="url_altera_rotativo"),
    
    #Mensalista
    path('cadastro_mensalista/', cadastro_mensalista, name='url_cadastro_mensalista'),
    path('lista_mensalista/', listagem_mensalista, name="url_lista_mensalista"),
    path('altera_mensalista/<int:id>/', altera_mensalista, name="url_altera_mensalista"),
    path('exclui_mensalista/<int:id>/', exclui_mensalista, name="url_exclui_mensalista"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

