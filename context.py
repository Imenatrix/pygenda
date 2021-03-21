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

        cursor = self.cursor

        cursor.execute(('select codigo, nome from agenda;'))
        qagendas = [agenda for agenda in cursor]

        cursor.execute(('select codigo, email from email;'))
        qemails = [email for email in cursor]

        cursor.execute(('select codigo, telefone from telefone;'))
        qtelefones = [telefone for telefone in cursor]

        agendas = {}

        for (codigo, nome) in qagendas:
            agendas[codigo] = Agenda(codigo, nome)

        for (codigo, email) in qemails:
            agendas[codigo].emails.append(email)

        for (codigo, telefone) in qtelefones:
            agendas[codigo].telefones.append(telefone)

        self.agendas = agendas

    def createAgenda(self, nome):
        
        cursor = self.cursor

        cursor.execute(('insert into agenda(nome) values (%s);'), (nome, ))
        codigo = cursor.lastrowid
        self.agendas[codigo] = Agenda(codigo, nome)
        self.connection.commit()

    def createEmail(self, codigo, email):

        cursor = self.cursor

        cursor.execute(('insert into email(codigo, email) values (%s, %s)'), (codigo, email))
        self.connection.commit()

    def createTelefone(self, codigo, telefone):
        
        cursor = self.cursor

        cursor.execute(('insert into telefone(codigo, telefone) values (%s, %s)'), (codigo, telefone))
        self.connection.commit()

    
    def drop(self):
        self.cursor.close()
        self.connection.close()