import json
from context import Context

# carrega configurações
with open('config.json') as file:
    config = json.load(file)

# conecta ao banco usando configurações
context = Context(
    user = config['usuario'],
    password = config['senha'],
    host = config['host'],
    database = config['schema']
)

codigo = input('Codigo: ')
email = input('Email: ')
context.createEmail(codigo, email)
for codigo, agenda in context.agendas.items():
    print(f'{codigo}: {agenda.nome} > {agenda.emails[len(agenda.emails) - 1] if len(agenda.emails) > 0 else ""}')

# fecha a conexão
context.drop()