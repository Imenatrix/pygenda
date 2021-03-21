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

codigo = int(input('Codigo: '))
telefone = input('Telefone: ')
context.createTelefone(codigo, telefone)
for codigo, agenda in context.agendas.items():
    print(f'{codigo}: {agenda.nome} > {agenda.telefones[len(agenda.telefones) - 1] if len(agenda.telefones) > 0 else ""}')

# fecha a conexão
context.drop()