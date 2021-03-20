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

for codigo, agenda in context.agendas.items():
    print(f'{codigo}: {agenda.nome}')

# fecha a conexão
context.drop()