from django.contrib import admin
from core.models import *

list = [Cliente, Fabricante, Veiculo, Preco, Mensalista, Rotativo, Forma_Pagamento]

admin.site.register(list)

# Register your models here.

"""admin.site.register(Cliente)
admin.site.register(Fabricante)
admin.site.register(Veiculo)
admin.site.register(Preco)
admin.site.register(Mensalista)
admin.site.register(Rotativo)"""