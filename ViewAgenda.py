import os
from getch import getch

def render(agenda):

    selection = 0

    while True:
        os.system('clear')
        print(f'Nome: {agenda.nome}')
        print('--------------------')
        if selection == 0:
            print('[ Emails ]  Telefones')
        elif selection == 1:
            print('  Emails  [ Telefones ]')
        print('--------------------')

        if selection == 0:
            for email in agenda.emails:
                print(email)
        elif selection == 1:
            for telefone in agenda.telefones:
                print(telefone)
        
        # entrada do teclado
        key = handleKeyboardInput()

        # busca por pelas setas
        if key == b'\x1b[C':
            selection += 1
            if selection == 2:
                selection = 0
        elif key == b'\x1b[D':
            selection -= 1
            if selection == -1:
                selection = 1

def handleKeyboardInput():
    key = getch()
    if bytes(key, 'utf-8') == b'\x1b':
        key += getch() + getch()
    return bytes(key, 'utf-8')