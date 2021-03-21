def render(agenda):
    print(f'Nome: {agenda.nome}')
    print('--------------------')
    print('[ Emails ] Telefones')
    print('--------------------')
    
    for email in agenda.emails:
        print(email)