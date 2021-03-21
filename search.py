def render(agendas):

    stragendas, strnomes, stremails = generateStringLists(agendas)

    mnome = max([len(nome) for nome in strnomes])
    memail = max([len(email) for email in stremails])

    for agenda in stragendas:
        print(agenda['nome'] + (mnome - len(agenda['nome'])) * ' ', end=' | ')
        print(agenda['email'] + (memail - len(agenda['email'])) * ' ', end=' | ')
        print(agenda['telefone'])

# gera as strings para renderização separadamente
# assim eu posso contar o tamanho de cada uma
# e ajustar o espaçamento da tabela dinamicamente
def generateStringLists(agendas):
    stragendas = []
    strnomes = []
    stremails = []

    for agenda in agendas:

        strnomes.append(agenda.nome)

        stremail = ''
        if len(agenda.emails) > 0:
            stremail = agenda.emails[0]
            if len(agenda.emails) > 1:
                stremail += f' (+{len(agenda.emails)})'
        stremails.append(stremail)

        strtelefone = ''
        if len(agenda.telefones) > 0:
            strtelefone = str(agenda.telefones[0])
            if len(agenda.telefones) > 1:
                strtelefone += f' (+{len(agenda.telefones)})'
        
        stragendas.append({
            'nome' : agenda.nome,
            'email' : stremail,
            'telefone' : strtelefone
        })

    return (stragendas, strnomes, stremails)