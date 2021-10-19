from select import select
from selenium import webdriver
import os 
import time
from selenium.webdriver.support.ui  import Select

# WEBSCRAPING
# ----------- 

lista_de_jogos = []

navegador = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'))

url = navegador.get('https://www.cbf.com.br/')

jogosHoje = navegador.find_element_by_xpath('//*[@id="app"]/header/div/nav/ul/li[3]/a/b').click()

jogosHojeTdos = navegador.find_element_by_xpath('//*[@id="app"]/header/div/nav/ul/li[3]/a').click()

# selecionando o campionanto dentro de um select 
jogosHojeSerieA = navegador.find_element_by_id('competition-filter')
selectElement = Select(jogosHojeSerieA)


selectElement.select_by_index(0)
jogos = navegador.find_elements_by_class_name('box')

for i in jogos:
    print(i.text)
    print(20 * '-')

