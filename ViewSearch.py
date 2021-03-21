from getch import getch
import os
import ViewAgenda

def render(agendas):

    stragendas, strnomes, stremails = generateStringLists(list(agendas.values()))

    mnome = max([len(nome) for nome in strnomes])
    memail = max([len(email) for email in stremails])

    selection = 0
    while True:

        os.system('clear')
        for i in range(len(stragendas)):
            agenda = stragendas[i]

            if i == selection:
                print('> ', end='')
            else:
                print('  ', end='')

            print(agenda['nome'] + (mnome - len(agenda['nome'])) * ' ', end=' | ')
            print(agenda['email'] + (memail - len(agenda['email'])) * ' ', end=' | ')
            print(agenda['telefone'])

        # entrada do teclado
        key = handleKeyboardInput()

        # busca por pelas setas
        if key == b'\n':
            ViewAgenda.render(agendas[
                stragendas[selection]['codigo']
            ])
            return render(agendas)
        elif key == b'\x1b[B':
            selection += 1
            if selection == len(stragendas):
                selection = 0
        elif key == b'\x1b[A':
            selection -= 1
            if selection == -1:
                selection = len(stragendas) - 1

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
            'codigo' : agenda.codigo,
            'nome' : agenda.nome,
            'email' : stremail,
            'telefone' : strtelefone
        })

    return (stragendas, strnomes, stremails)

def handleKeyboardInput():
    key = getch()
    if bytes(key, 'utf-8') == b'\x1b':
        key += getch() + getch()
    return bytes(key, 'utf-8')