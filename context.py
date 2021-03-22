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

        cursor.execute(('select codigo, nome from agenda'))
        qagendas = [agenda for agenda in cursor]

        cursor.execute(('select codigo, email from email'))
        qemails = [email for email in cursor]

        cursor.execute(('select codigo, telefone from telefone'))
        qtelefones = [telefone for telefone in cursor]

        agendas = {}

        for (codigo, nome) in qagendas:
            agendas[codigo] = Agenda(codigo, nome)

        for (codigo, email) in qemails:
            agendas[codigo].emails.append(email)

        for (codigo, telefone) in qtelefones:
            agendas[codigo].telefones.append(telefone)

        self.agendas = agendas

    def createAgenda(self, agenda):
        self.cursor.execute(
            ('insert into agenda(nome) values (%s)'),
            (agenda.nome, )
        )
        agenda.codigo = self.cursor.lastrowid
        self.agendas[agenda.codigo] = agenda
        self.connection.commit()

    def updateAgenda(self, agenda):
        self.cursor.execute(
            ('update agenda set nome = %s where codigo = %s'),
            (agenda.nome, agenda.codigo)
        )
        self.agendas[agenda.codigo].nome = agenda.nome
        self.connection.commit()

    def deleteAgenda(self, agenda):
        for email in agenda.emails:
            self.cursor.execute(
                ('delete from email where codigo = %s and email = %s'),
                (agenda.codigo, email)
            )

        for telefone in agenda.telefones:
            self.cursor.execute(
                ('delete from telefone where codigo = %s and telefone = %s'),
                (agenda.codigo, telefone)
            )

        self.cursor.execute(
            ('delete from agenda where codigo = %s'),
            (agenda.codigo, )
        )

        self.agendas.pop(agenda.codigo)
        self.connection.commit()

    def createEmail(self, codigo, email):
        self.cursor.execute(
            ('insert into email(codigo, email) values (%s, %s)'),
            (codigo, email)
        )
        self.agendas[codigo].emails.append(email)
        self.connection.commit()

    def updateEmail(self, codigo, email, newEmail):
        self.cursor.execute(
            ('update email set email = %s where codigo = %s and email = %s'),
            (newEmail, codigo, email)
        )
        index = self.agendas[codigo].emails.index(email)
        self.agendas[codigo].emails[index] = newEmail
        self.connection.commit()

    def deleteEmail(self, codigo, email):
        self.cursor.execute(
            ('delete from email where codigo = %s and email = %s'),
            (codigo, email)
        )
        self.agendas[codigo].emails.remove(email)
        self.connection.commit()

    def createTelefone(self, codigo, telefone):
        self.cursor.execute(
            ('insert into telefone(codigo, telefone) values (%s, %s)'),
            (codigo, telefone)
        )
        self.agendas[codigo].telefones.append(telefone)
        self.connection.commit()

    def updateTelefone(self, codigo, telefone, newTelefone):
        self.cursor.execute(
            ('update telefone set telefone = %s where codigo = %s and telefone = %s'),
            (newTelefone, codigo, telefone)
        )
        index = self.agendas[codigo].telefones.index(telefone)
        self.agendas[codigo].telefones[index] = newTelefone
        self.connection.commit()

    def deleteTelefone(self, codigo, telefone):
        self.cursor.execure(
            ('delete from telefone where codigo = %s and telefone = %s'),
            (codigo, telefone)
        )
        self.agendas[codigo].telefones.remove(telefone)
        self.connection.commit()
    
    def drop(self):
        self.cursor.close()
        self.connection.close()