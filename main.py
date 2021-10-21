# importações
from selenium import webdriver
import os 
from selenium.webdriver.support.ui  import Select
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# FAZENDO O WEBSCRAPING

# listas e dicionário
deletar = []
aux = []
dados = {'times': [],
         'horario': []}

# conectando o navegador
navegador = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'))

# link de acesso 
url = navegador.get('https://www.cbf.com.br/')

# navegando pelo site
jogosHoje = navegador.find_element_by_xpath('//*[@id="app"]/header/div/nav/ul/li[3]/a/b').click()
jogosHojeTdos = navegador.find_element_by_xpath('//*[@id="app"]/header/div/nav/ul/li[3]/a').click()

# selecionando o campionanto dentro de um select 
jogosHojeSerieA = navegador.find_element_by_id('competition-filter')
selectElement = Select(jogosHojeSerieA)

selectElement.select_by_index(0)
jogos = navegador.find_elements_by_class_name('clearfix')

# adicionando os jogos com o horário do jogo na lista auxiliar
for i in jogos:
    jogo = i.text
    deletar.append(str(jogo).replace('\n', ' '))

    aux = deletar[1:-1]
   
'''
 fazendo uma sequência de condições para acessar os jogos
  e a horas e adicionando ao dicionário
'''
for i in aux:
    info = str(i).split()

    if info[0] != '-' and info[1] != '-' and info[2] != '-':
        time1 = info[0] + ' ' + info[1] + ' ' + info[2]
        if info[6] != '-' and info[7] != '-' and info[8] != '-':
            time2 = info[6] + ' ' + info[7] + ' ' + info[8]
            dados['times'].append(time1 + ' x ' + time2)
            dados['horario'].append(info[5])
        elif info[6] != '-' and info[7] != '-':
            time2 = info[6] + ' ' + info[7]
            dados['times'].append(time1 + ' x ' + time2)
            dados['horario'].append(info[5])
        else:
            time2 = info[6] 
            dados['times'].append(time1 + ' x ' + time2)
            dados['horario'].append(info[5])
    elif info[0] and info[1] != '-':
        time1 = info[0] + ' ' + info[1]
        if info[5] != '-' and info[6] != '-' and info[7] != '-':
            time2 = info[5] + ' ' + info[6] + ' ' + info[7]
            dados['times'].append(time1 + ' x ' + time2)
            dados['horario'].append(info[4])
        elif info[5] != '-' and info[6] != '-':
            time2 = info[5] + ' ' + info[6]
            dados['times'].append(time1 + ' x ' + time2)
            dados['horario'].append(info[4])
        else:
            time2 = info[5] 
            dados['times'].append(time1 + ' x ' + time2)
            dados['horario'].append(info[4])
    elif info[0] != '-':
        time1 = info[0]
        if info[4] != '-' and info[5] != '-' and info[6] != '-':
            time2 = info[4] + ' ' + info[5] + ' ' + info[6]
            dados['times'].append(time1 + ' x ' + time2)
            dados['horario'].append(info[3])
        elif info[4] != '-' and info[5] != '-':
            time2 = info[4] + ' ' + info[5]
            dados['times'].append(time1 + ' x ' + time2)
            dados['horario'].append(info[3])
        else:
            time2 = info[4] 
            dados['times'].append(time1 + ' x ' + time2)
            dados['horario'].append(info[3])

# fechando o navegador
navegador.close()

# USANDO PANDAS
df = pd.DataFrame(dados)

arquivo = df[['horario', 'times']].groupby(['horario', 'times']).max()
arquivo.to_csv('jogos_do_dia')

# ENVIANDO O EMAIL 

# configurando variáveis e iniciando o servidor
host = 'smtp.gmail.com'
port = 587 
user = 'remetente'
password = 'senha'

server = smtplib.SMTP(host=host, port=port)

server.ehlo()
server.starttls()
server.login(user, password)

# partes do email 
message = MIMEMultipart()
message['From'] = user
message['To'] = 'destinatario'
message['Subject'] = 'Jogos do dia'

# fixando mensagem ao email
message.attach(MIMEText('''
    Olá! Segue a lista dos jogos do dia de hoje :)
''', 'plain'))

# parte do anexo
filename = 'jogos_do_dia'
attachment = open('jogos_do_dia', 'rb')

att = MIMEBase('application', 'octet-stream')
att.set_payload(attachment.read())
encoders.encode_base64(att)

att.add_header('Content-Disposition', f'attachment; filename= {filename}')
attachment.close()
message.attach(att)

# enviando o emil
try:
    server.sendmail(message['From'], message['To'], message.as_string())
    print('Email enviado com sucesso!')
except Exception as e:
    print(e)

# fechando o servidor de email
server.quit()
