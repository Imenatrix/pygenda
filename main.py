import json
from context import Context
import agenda

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

agenda.render(list(context.agendas.values())[0])

# fecha a conexão
context.drop()