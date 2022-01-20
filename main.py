import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
import time
import email
import imaplib
import uuid

#Acessos

smtphost='smtp.gmail.com'
smtpport=587
senderuser= 'espian.python@gmail.com'
senderpassword= 'Espian@python'

imaphost = 'imap.gmail.com'
reciuser = 'espian.python.rec@gmail.com'
recipassword = 'Espian@python'


class EnvRec():
    global subject
    subject = str(uuid.uuid4())

    def envio(self):
        print('Criando acesso')
        server= smtplib.SMTP(smtphost,smtpport)

        print('Login...')
        server.ehlo()
        server.starttls()
        server.login(senderuser,senderpassword)

        #mensagem
        message= 'Teste'
        print('Criando Mensagem...')
        self.email_msg= MIMEMultipart()
        self.email_msg['From']= senderuser
        self.email_msg['To']= reciuser
        self.email_msg['Subject']= subject
        self.email_msg['Message-id']= email.utils.make_msgid()

        print('adicionando texto')
        self.email_msg.attach(MIMEText(message,'plain'))

        #enviando mensagem

        print('Enviando Mensagem...')
        server.sendmail(self.email_msg['From'],self.email_msg['To'],self.email_msg.as_string())
        print('Mensagem enviada!')
        print(subject)
        print('=============================================================================')
        server.quit()


    def recebimento(self):
        print('Acessando Imap')
        mail = imaplib.IMAP4_SSL(imaphost)
        mail.login(reciuser, recipassword)
        mail.list()
        mail.select('inbox')
        for i in range(5):
            try:
                print("Tentando Ler")
                result, data = mail.search(None, 'SUBJECT', '%s' %subject)
                ids = data[0]
                id_list = ids.split()
                result, data = mail.fetch(id_list[0], "(RFC822)")
                raw_email = data[0][1]
                print(result)
                print(subject)
                break
            except:
                print("Aguardando...")
                time.sleep(10)


EnvRec().envio()
EnvRec().recebimento()



