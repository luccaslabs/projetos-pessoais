from db import conectar

class Produtos():
    def __init__(self):
        pass

    def cadastrar_produtos(self, nome, valor, estoque):
        if estoque < 0:
            print("Estoque não pode ser negativo")
            return
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "INSERT INTO produtos (nome, valor, estoque) VALUES (%s, %s, %s)"
        valores = (nome, valor, estoque) 
        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()
        conexao.close()
        print(f"Produto {nome} cadastrado com sucesso!")

    def listar_produtos(self):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, estoque FROM produtos")
        produtos = cursor.fetchall()
        for p in produtos:
            print(f"ID: {p[0]} | NOME: {p[1]} | ESTOQUE: {p[2]}")
        cursor.close()
        conexao.close()

    def dar_baixa_estoque(self, id_produto, quantidade):
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "UPDATE produtos SET estoque = estoque - %s WHERE id = %s AND estoque >= %s"
        valores = (quantidade, id_produto, quantidade)
        cursor.execute(sql, valores)
        conexao.commit()
        if cursor.rowcount == 0:
            print("Estoque insuficiente ou produto não encontrado.")
        else:
            print("Baixa realizada com sucesso!")
        cursor.close()
        conexao.close()

    def repor_estoque(self, id_produto, quantidade):
        if quantidade <= 0:
            print("Quantidade inválida!")
            return
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "UPDATE produtos SET estoque = estoque + %s WHERE id = %s"
        valores = (quantidade, id_produto)
        cursor.execute(sql, valores)
        conexao.commit()
        if cursor.rowcount == 0:
            print("Produto não encontrado.")
        else:
            print("Reposição realizada com sucesso!")
        cursor.close()
        conexao.close()