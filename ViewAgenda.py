import os
from getch import getch

def render(agenda):

    mode = 0
    hselection = 0
    vselection = -1

    while True:
        os.system('clear')

        if vselection == -1:
            print('> ', end='')
        else:
            print('  ', end='')
        print(f'Nome: {agenda.nome}')
        print('--------------------')
        if hselection == 0:
            print('[ Emails ]  Telefones')
        elif hselection == 1:
            print('  Emails  [ Telefones ]')
        print('--------------------')

        if hselection == 0:
            for i in range(len(agenda.emails)):
                email = agenda.emails[i]
                if i == vselection:
                    print('> ', end='')
                else:
                    print('  ', end='')
                print(email)
        elif hselection == 1:
            for i in range(len(agenda.telefones)):
                telefone = agenda.telefones[i]
                if i == vselection:
                    print('> ', end='')
                else:
                    print('  ', end='')
                print(telefone)
        
        # entrada do teclado
        key = handleKeyboardInput()

        if mode == 0:
            # busca por pelas setas
            if key == b'\x1b[C':
                hselection += 1
                if hselection == 2:
                    hselection = 0
                vselection = -1
            elif key == b'\x1b[D':
                hselection -= 1
                if hselection == -1:
                    hselection = 1
                vselection = -1
            elif key == b'\x1b[B':
                if vselection < len(agenda.emails if hselection == 0 else agenda.telefones) - 1:
                    vselection += 1
            elif key == b'\x1b[A':
                if vselection > -1:
                    vselection -= 1
            # busca por backspace
            elif key == b'\x7f':
                return
            elif key == b'\n':
                mode = 1
        elif mode == 1:
            if vselection == -1:
                if key == b'\x7f':
                    agenda.nome = agenda.nome[:-1]
                if key.decode('utf-8').isprintable():
                    agenda.nome += key.decode('utf-8')
            else:
                if hselection == 0:
                    if key == b'\x7f':
                        agenda.emails[vselection] = agenda.emails[vselection][:-1]
                    if key.decode('utf-8').isprintable():
                        agenda.emails[vselection] += key.decode('utf-8')
                elif hselection == 1:
                    if key == b'\x7f':
                        agenda.telefones[vselection] = int(str(agenda.telefones[vselection])[:-1])
                    if key.decode('utf-8').isdigit():
                        agenda.telefones[vselection] = int(str(agenda.telefones[vselection]) + key.decode('utf-8'))
            if key == b'\n':
                mode = 0

def handleKeyboardInput():
    key = getch()
    if bytes(key, 'utf-8') == b'\x1b':
        key += getch() + getch()
    return bytes(key, 'utf-8')