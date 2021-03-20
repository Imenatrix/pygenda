import json
import mysql.connector

class Agenda:

    def __init__(self, codigo, nome):
        self.codigo = codigo
        self.nome = nome
        self.telefones = []
        self.emails = []

# carrega configurações
with open('config.json') as file:
    config = json.load(file)

# conecta ao banco usando configurações
cnx = mysql.connector.connect(
    user = config['usuario'],
    password = config['senha'],
    host = config['host'],
    database = config['schema']
)
cursor = cnx.cursor()

cursor.execute(('select codigo, nome from agenda;'))
qagendas = [agenda for agenda in cursor]

cursor.execute(('select codigo, email from email;'))
qemails = [email for email in cursor]

cursor.execute(('select codigo, telefone from telefone;'))
qtelefones = [telefone for telefone in cursor]

agendas = {}

for (codigo, nome) in qagendas:
    agendas[codigo] = Agenda(codigo, nome)

for (codigo, email) in qemails:
    agendas[codigo].emails.append(email)

for (codigo, telefone) in qtelefones:
    agendas[codigo].telefones.append(telefone)

for codigo, agenda in agendas.items():
    print(agenda.nome)
    print(agenda.emails)
    print(agenda.telefones)
    print()

# fecha a conexão
cursor.close()
cnx.close()