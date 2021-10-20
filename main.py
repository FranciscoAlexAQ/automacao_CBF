from select import select
from selenium import webdriver
import os 
import time
from selenium.webdriver import chrome
from selenium.webdriver.support.ui  import Select
from selenium.webdriver.chrome.options import Options
import pandas

# WEBSCRAPING
# ----------- 

deletar = []
aux = []
dados = {'times': [],
         'horario': []}

navegador = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'))

url = navegador.get('https://www.cbf.com.br/')

jogosHoje = navegador.find_element_by_xpath('//*[@id="app"]/header/div/nav/ul/li[3]/a/b').click()

jogosHojeTdos = navegador.find_element_by_xpath('//*[@id="app"]/header/div/nav/ul/li[3]/a').click()

# selecionando o campionanto dentro de um select 
jogosHojeSerieA = navegador.find_element_by_id('competition-filter')
selectElement = Select(jogosHojeSerieA)


selectElement.select_by_index(0)
jogos = navegador.find_elements_by_class_name('clearfix')

for i in jogos:
    jogo = i.text
    deletar.append(str(jogo).replace('\n', ' '))

    aux = deletar[1:-1]
   

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

# USANDO PANDAS

df = pandas.DataFrame(dados)
df.to_csv('jogos_do_dia')
