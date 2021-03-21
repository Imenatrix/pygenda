import json
from context import Context
import ViewSearch

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

ViewSearch.render(context, context.agendas)

# fecha a conexão
context.drop()