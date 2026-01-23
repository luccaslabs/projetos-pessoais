from banco import Banco, Cliente
banco = Banco()

while True:
    print("\n--- MENU ---")
    print("1 - Cadastrar cliente")
    print("2 - Ver saldo")
    print("3 - Sacar")
    print("4 - Depositar")
    print("5 - Listar Clientes")
    print("0 - Sair")

    opcao = int(input("Digite a opção desejada: "))

    match opcao:
        case 1:
            nome = str(input("Digite o nome do cliente: "))
            saldo = float(input("Digite o saldo inicial: "))
            banco.cadastrar_cliente(nome, saldo)
        
        case 2:
            nome = str(input("Digite o nome do cliente: "))
            cliente = banco.buscar_cliente(nome)
            if cliente:
                cliente.ver_saldo()
            else:
                print("Cliente não encontrado!")

        case 3:
            nome = str(input("Digite o nome do cliente: "))
            cliente = banco.buscar_cliente(nome)
            if cliente:
                valor = float(input("Digite o valor que deseja sacar: "))
                cliente.sacar(valor)
            else:
                print("Cliente não encontrado!")
        
        case 4:
            nome = str(input("Digite o nome do cliente: "))
            cliente = banco.buscar_cliente(nome)
            if cliente:
                valor = float(input("Valor do depósito: "))
                Cliente.depositar(valor)
            else:
                print("Cliente não encontrado!")

        case 5:
            banco.listar_clientes()

        case 0:
            break
            
            
            