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

    def createAgenda(self, agenda):
        
        cursor = self.cursor

        cursor.execute(('insert into agenda(nome) values (%s);'), (agenda.nome, ))
        agenda.codigo = cursor.lastrowid
        self.agendas[agenda.codigo] = agenda

        self.connection.commit()

    def updateAgenda(self, agenda):

        cursor = self.cursor

        cursor.execute(('update agenda set nome = %s where codigo = %s'), (agenda.nome, agenda.codigo))
        self.connection.commit()

    def deleteAgenda(self, agenda):

        cursor = self.cursor

        cursor.execure(('delete from agenda where codigo = %s'), (agenda.codigo, ))
        self.connection.commit()


    def createEmail(self, codigo, email):

        cursor = self.cursor

        cursor.execute(('insert into email(codigo, email) values (%s, %s)'), (codigo, email))
        self.agendas[codigo].emails.append(email)
        self.connection.commit()

    def updateEmail(self, codigo, email, newEmail):

        cursor = self.cursor

        cursor.execute(('update email set email = %s where codigo = %s and email = %s'), (newEmail, codigo, email))
        index = self.agendas[codigo].emails.index(email)
        self.agendas[codigo].emails[index] = newEmail
        self.connection.commit()

    def deleteEmail(self, codigo, email):

        cursor = self.cursor

        cursor.execute(('delete from email where codigo = %s and email = %s'), (codigo, email))
        self.agendas[codigo].emails.remove(email)
        self.connection.commit()

    def createTelefone(self, codigo, telefone):
        
        cursor = self.cursor

        cursor.execute(('insert into telefone(codigo, telefone) values (%s, %s)'), (codigo, telefone))
        self.agendas[codigo].telefones.append(telefone)
        self.connection.commit()

    def updateTelefone(self, codigo, telefone, newTelefone):

        cursor = self.cursor

        cursor.execute(('update telefone set telefone = %s where codigo = %s and telefone = %s'), (newTelefone, codigo, telefone))
        index = self.agendas[codigo].telefones.index(telefone)
        self.agendas[codigo].telefones[index] = newTelefone
        self.connection.commit()

    def deleteTelefone(self, codigo, telefone):

        cursor = self.cursor
        cursor.execure(('delete from telefone where codigo = %s and telefone = %s'), (codigo, telefone))
        self.agendas[codigo].telefones.remove(telefone)
        self.connection.commit()

    
    def drop(self):
        self.cursor.close()
        self.connection.close()