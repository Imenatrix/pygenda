import mysql.connector

class Agenda:

    def __init__(self, codigo, nome):
        self.codigo = codigo
        self.nome = nome
        self.telefones = []
        self.emails = []

class Context:

    def __init__(self, user, password, host, database):
        self.connection = mysql.connector.connect(
            user = user,
            password = password,
            host = host,
            database = database
        )
        self.cursor = self.connection.cursor()
        self.load()

    def load(self):
        self.cursor.execute(('select codigo, nome from agenda;'))
        qagendas = [agenda for agenda in self.cursor]

        self.cursor.execute(('select codigo, email from email;'))
        qemails = [email for email in self.cursor]

        self.cursor.execute(('select codigo, telefone from telefone;'))
        qtelefones = [telefone for telefone in self.cursor]

        agendas = {}

        for (codigo, nome) in qagendas:
            agendas[codigo] = Agenda(codigo, nome)

        for (codigo, email) in qemails:
            agendas[codigo].emails.append(email)

        for (codigo, telefone) in qtelefones:
            agendas[codigo].telefones.append(telefone)

        self.agendas = agendas
    
    def drop(self):
        self.cursor.close()
        self.connection.close()