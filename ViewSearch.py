from getch import getch
import os
import contextlib
import ViewAgenda
from context import Agenda
from fuzzywuzzy import process

def render(context, agendas, selection = -1):

    term = ''
    while True:

        # https://stackoverflow.com/questions/8391411/how-to-block-calls-to-print
        # suprime stderr temporariamente
        # se temp == '' ou outros casos especificos,
        # fuzzywuzzy.process imprime avisos sobre otimizações
        with open(os.devnull, "w") as f, contextlib.redirect_stderr(f):
            nomes, emails, telefones = search(term, agendas.values())

        stragendas, strnomes, stremails = generateStringLists(
            sort(
                agendas.values(),
                nomes,
                emails,
                telefones
            ),
            emails,
            telefones,
        )

        mnome = max([len(nome) for nome in strnomes]) if len(strnomes) != 0 else 0
        memail = max([len(email) for email in stremails]) if len(stremails) != 0 else 0

        os.system('clear')

        print('<SETAS : NAVEGAR> | <ENTER : SELECIONAR> | <DEL : REMOVER> | <TAB : SAIR>')
        print()

        print(f'Digite para buscar: {term}\u2588')
        print()
        
        if selection == -1:
            print('> ', end='')
        else:
            print('  ', end='')
        print('[Novo]')
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
            if selection == -1:
                ViewAgenda.render(context, Agenda(None, ''))
            else:
                ViewAgenda.render(context, agendas[
                    stragendas[selection]['codigo']
                ])
            return render(context, agendas, selection)
        elif key == b'\x1b[3~':
            if selection != -1:
                context.deleteAgenda(agendas[
                    stragendas[selection]['codigo']
                ])
                if selection >= len(stragendas) - 1:
                    selection -= 1
                return render(context, agendas, selection)
        elif key == b'\x1b[B':
            if selection < len(stragendas) - 1:
                selection += 1
        elif key == b'\x1b[A':
            if selection > -1:
                selection -= 1

        # sair
        elif key == b'\t':
                return

        # apaga caracter
        if key == b'\x7f':
            term = term[:-1]
        # adiciona caracter
        elif key.decode('utf-8').isprintable():
            term = term + key.decode('utf-8')

def search(term, agendas):

    nomes = {}
    emails = {}
    telefones = {}

    for agenda in agendas:
        nomes[agenda.codigo] = agenda.nome
        emails[agenda.codigo] = process.extract(term, agenda.emails)
        telefones[agenda.codigo] = process.extract(term, [str(telefone) for telefone in agenda.telefones])
    
    for score in process.extract(term, nomes):
        nomes[score[2]] = (score[0], score[1])

    return (nomes, emails, telefones)

def sort(agendas, nomes, emails, telefones):
    return sorted(agendas, reverse=True, key = lambda agenda : nomes[agenda.codigo][1] + coiso(emails[agenda.codigo]) + coiso(telefones[agenda.codigo]))

def coiso(treco):
    return treco[0][1] if len(treco) > 0 else 0

# gera as strings para renderização separadamente
# assim eu posso contar o tamanho de cada uma
# e ajustar o espaçamento da tabela dinamicamente
def generateStringLists(agendas, emails, telefones):
    stragendas = []
    strnomes = []
    stremails = []

    for agenda in agendas:

        strnomes.append(agenda.nome)

        stremail = ''
        if len(agenda.emails) > 0:
            stremail = emails[agenda.codigo][0][0]
            if len(agenda.emails) > 1:
                stremail += f' (+{len(agenda.emails)})'
        stremails.append(stremail)

        strtelefone = ''
        if len(agenda.telefones) > 0:
            strtelefone = telefones[agenda.codigo][0][0]
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
        if bytes(key, 'utf-8') == b'\x1b[3':
            key += getch()
    return bytes(key, 'utf-8')