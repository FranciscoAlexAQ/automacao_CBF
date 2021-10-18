from select import select
from selenium import webdriver
import os 
import time
from selenium.webdriver.support.ui  import Select

# WEBSCRAPING
# ----------- 

navegador = webdriver.Chrome(executable_path=os.path.abspath('chromedriver'))

url = navegador.get('https://www.cbf.com.br/')

jogosHoje = navegador.find_element_by_xpath('//*[@id="app"]/header/div/nav/ul/li[3]/a/b').click()

jogosHojeTdos = navegador.find_element_by_xpath('//*[@id="app"]/header/div/nav/ul/li[3]/a').click()

# selecionando o campionanto dentro de um select 
jogosHojeSerieA = navegador.find_element_by_id('competition-filter')
selectElement = Select(jogosHojeSerieA)
selectElement.select_by_value('Campeonato Brasileiro de Futebol - Série A 2021')
