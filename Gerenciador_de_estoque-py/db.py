import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '12345678',
        database = 'gerenciador' 
        )
    return conexao
