import os
from getch import getch

def render(context, agenda):

    mode = 0
    hselection = 0
    vselection = -2

    newEmail = ''
    newTelefone = ''

    while True:
        os.system('clear')

        if vselection == -2:
            print('> ', end='')
        else:
            print('  ', end='')

        print(f'Nome: {agenda.nome}', end='')
        print('\u2588' if mode == 1 and vselection == -2 else '')
        print('--------------------')

        if hselection == 0:
            print('[ Emails ]  Telefones')
        elif hselection == 1:
            print('  Emails  [ Telefones ]')
        print('--------------------')

        if mode == 0:
            if vselection == -1:
                print('> ', end='')
            else:
                print('  ', end='')
            print('[Novo]')
        elif mode == 1:
            if vselection == -1:
                print('> ', end='')
                if hselection == 0:
                    print(f'{newEmail}\u2588')
                elif hselection == 1:
                    print(f'{newTelefone}\u2588')

        if hselection == 0:
            for i in range(len(agenda.emails)):
                email = agenda.emails[i]
                if i == vselection:
                    print('> ', end='')
                    if mode == 0:
                        print(email)
                    elif mode == 1:
                        print(f'{newEmail}\u2588')
                else:
                    print('  ', end='')
                    print(email)
        elif hselection == 1:
            for i in range(len(agenda.telefones)):
                telefone = agenda.telefones[i]
                if i == vselection:
                    print('> ', end='')
                    if mode == 0:
                        print(telefone)
                    elif mode == 1:
                        print(f'{newTelefone}\u2588')
                else:
                    print('  ', end='')
                    print(telefone)
        
        # entrada do teclado
        key = handleKeyboardInput()

        # modo de seleção
        if mode == 0:
            # baixo
            if key == b'\x1b[A' and vselection > -2:
                    vselection -= 1
            # cima
            elif key == b'\x1b[B' and vselection < len(agenda.emails if hselection == 0 else agenda.telefones) - 1:
                    vselection += 1
            # direita
            elif key == b'\x1b[C':
                hselection += 1
                vselection = -2
                if hselection == 2:
                    hselection = 0
            # esquerda
            elif key == b'\x1b[D':
                hselection -= 1
                vselection = -2
                if hselection == -1:
                    hselection = 1

            # sair
            elif key == b'\x7f':
                return

            # editar
            elif key == b'\n':
                mode = 1
                
                # email
                if hselection == 0:
                    if vselection > -1:
                        newEmail = agenda.emails[vselection]
                    elif vselection == -1:
                        newEmail = ''

                # telefone
                elif hselection == 1:
                    if vselection > -1: # novo
                        telefone = agenda.telefones[vselection]
                    elif vselection == -1:
                        newTelefone = ''

        # modo de edição
        elif mode == 1:
            # nome
            if vselection == -2:

                # apaga caracter
                if key == b'\x7f':
                    agenda.nome = agenda.nome[:-1]
                # adiciona caracter
                elif key.decode('utf-8').isprintable():
                    agenda.nome += key.decode('utf-8')

                # salva
                elif key == b'\n':
                    if agenda.codigo == None:
                        context.createAgenda(agenda)
                    else:
                        context.updateAgenda(agenda)
            # email
            elif hselection == 0:

                # apaga caracter
                if key == b'\x7f':
                    newEmail = newEmail[:-1]
                #adiciona caracter
                elif key.decode('utf-8').isprintable():
                    newEmail += key.decode('utf-8')

                # salva
                if key == b'\n':
                    if vselection == -1: # novo
                        context.createEmail(agenda.codigo, newEmail)
                    else:
                        context.updateEmail(agenda.codigo, agenda.emails[vselection], newEmail)
            
            # telefone
            elif hselection == 1:

                # apaga caracter
                if key == b'\x7f':
                    newTelefone = newTelefone[:-1]
                # adiciona caracter
                elif key.decode('utf-8').isdigit():
                    newTelefone = newTelefone + key.decode('utf-8')

                # salva
                if key == b'\n':
                    if vselection == -1: # novo
                        context.createTelefone(agenda.codigo, newTelefone)
                    else:
                        context.updateTelefone(agenda.codigo, agenda.telefones[vselection], newTelefone)
            if key == b'\n':
                mode = 0

def handleKeyboardInput():
    key = getch()
    if bytes(key, 'utf-8') == b'\x1b':
        key += getch() + getch()
    return bytes(key, 'utf-8')