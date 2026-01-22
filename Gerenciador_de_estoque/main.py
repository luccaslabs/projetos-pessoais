from produtos import Produtos

banco = Produtos()

while True:
    print("\n--- MENU ---")
    print("1 - Cadastrar produtos")
    print("2 - Ver estoque")
    print("3 - Dar baixa estoque")
    print("4 - Repor estoque")
    print("0 - Sair")

    opcao = int(input("Digite a opção desejada: "))

    match opcao:
        case 1:
            nome = str(input("Digite o nome do produto: "))
            valor = float(input("Digite o valor: "))
            estoque = int(input("Digite a quantidade em estoque: "))
            banco.cadastrar_produtos(nome, valor, estoque)
        
        case 2:
            banco.listar_produtos()

        case 3:
            id_produto_baixa = int(input("Digite o id do produto desejado: "))
            baixa_estoque = int(input("Digite a saída: "))
            banco.dar_baixa_estoque(id_produto_baixa, baixa_estoque)

        case 4:
            id_produto_repor = int(input("Digite o id do produto desejado: "))
            quantidade_repor = int(input("Digite a quantidade: "))
            banco.repor_estoque(id_produto_repor, quantidade_repor)
            

        case 0:
            break

            
