import json
import mysql.connector

# pega configurações do arquivo de configuração
with open('config.json') as file:
    config = json.load(file)

# conecta ao banco usando configurações
cnx = mysql.connector.connect(
    user = config['usuario'],
    password = config['senha'],
    host = config['host'],
    database = config['schema']
)

# fecha a conecção
cnx.close()