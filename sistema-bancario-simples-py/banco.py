class Cliente:
    def __init__(self, nome, saldo=0.0):
        self.nome = nome
        self.saldo = saldo

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print("Deposito realizado com sucesso!")
        else:
            print("Valor inválido")

    def sacar(self, saque):
        if saque > 0 and saque <= self.saldo:
            self.saldo -= saque
            print("Saque realizado com sucesso!")
        else:
            print("Erro ao tentar sacar o valor solicitado")

    def ver_saldo(self):
        print(f"Saldo de {self.nome}: R$ {self.saldo}")




class Banco:
    def __init__(self):
        print("Banco carregado")
        self.clientes = {}

    def cadastrar_cliente(self, nome, saldo_inicial):
        if nome in self.clientes:
            print("Cliente já cadastrado!")
        else:
            self.clientes[nome] = Cliente(nome, saldo_inicial)

    def buscar_cliente(self, nome):
        return self.clientes.get(nome)
    
    def listar_clientes(self):
        if not self.clientes:
            print("Cliente não cadastrado!")
        else:
            print("\nLista de Clientes:")
            for cliente in self.clientes.values():
                cliente.ver_saldo()