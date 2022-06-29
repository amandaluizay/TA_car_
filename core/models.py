from distutils.command.upload import upload
from email.policy import default
from math import ceil, floor, trunc
from optparse import BadOptionError
from pyexpat import model
from tabnanny import verbose
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    endereco = models.CharField(max_length=100, blank=True, null=True)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=50, blank=True, null=True)
    foto =models.ImageField(upload_to='fotos_clientes', blank=True, null=True)
    
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name_plural = 'Clientes'

class Fabricante(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao
    class Meta:
        verbose_name_plural = 'Fabricantes'

class Veiculo(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField(default=2022, blank=True, null=True)
    cor = models.CharField(max_length=50, blank=True, null=True)
    placa = models.CharField(max_length=10)
    foto =models.ImageField(upload_to='fotos_veiculos', blank=True, null=True)

    def __str__(self):
        return f'{self.placa} ({self.modelo})'
    class Meta:
        verbose_name_plural = 'Veiculos'

class Preco(models.Model):
    descricao = models.CharField(max_length=50, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")

    def __str__(self):
        return f'{self.descricao} - R$ {self.valor}'
    class Meta:
        verbose_name_plural = 'Tabela'

class Forma_Pagamento(models.Model):
    descricao = models.CharField(max_length=30, verbose_name="Forma de pagamento")

    def __str__(self): return self.descricao
    class Meta: verbose_name_plural = "Forma de pagamento"

class Mensalista(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    id_preco = models.ForeignKey(Preco, on_delete=models.CASCADE, verbose_name="Preço")
    dia_vencimento = models.IntegerField(default=5, verbose_name="Dia de vencimento")
    pendencia = models.BooleanField(blank=True, null=True,verbose_name="Pendência")
    forma_pagamento = models.ForeignKey(Forma_Pagamento, on_delete=models.CASCADE, verbose_name='Forma de pagamento', blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Valor com desconto")

    def __str__(self):
        return f"{self.id_cliente} - {self.id_preco}"
    class Meta:
        verbose_name_plural = 'Mensalista'
    
    """
        5% de desconto no dinheiro
        7% no pix
    """
    def desconto(self):
        obj = Forma_Pagamento.objects.get(id=self.forma_pagamento.pk)
        obj2 = Preco.objects.get(id=self.id_preco.pk)
        
        if obj.descricao == 'Dinheiro': total = float(obj2.valor) * 0.95
        elif obj.descricao == 'PIX': total = float(obj2.valor) * 0.93
        else: total = obj2.valor
        self.total = total
        return total

class Rotativo(models.Model):
    id_veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, verbose_name="Veiculo")
    id_preco = models.ForeignKey(Preco, on_delete=models.CASCADE, verbose_name="Preço")
    data_entrada = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Entrada")
    data_saida = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name="Saída")
    pago = models.BooleanField(default=False, blank=True, null=True, verbose_name="Pago")
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Total")
    
    def __str__(self):
        return f"{self.id_veiculo} - {self.data_entrada}"
    
    class Meta:
        verbose_name_plural = 'Rotativo'
    
    def calcula_total(self):
        if self.data_saida:
            horas = (self.data_saida - self.data_entrada).total_seconds()/3600
            obj = Preco.objects.get(id=self.id_preco.pk)
            adicional = 0.60 * float(obj.valor)

            if horas <= 0.5: taxa = float(obj.valor) / 2
            else:
                tolerancia = (horas) - trunc(horas)
                if tolerancia <=0.25:
                    taxa = float(obj.valor) + ((floor(horas-1)) * adicional)
                else:
                    taxa = float(obj.valor) + ((ceil(horas -1)) * adicional)

            self.total = taxa
            return True
        else: return False
