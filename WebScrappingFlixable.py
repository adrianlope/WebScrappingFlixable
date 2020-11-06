from selenium.webdriver.chrome.options import Options 
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import os.path
import re

minyear= input("¿Año comienzo de los datos? ")
maxyear= input("¿Año fin de los datos? ")
rating = input("¿puntuación mínima en imdb? ")

urlNetflix = 'https://es.flixable.com/?min-rating=' + rating +'&min-year='+ minyear +'&max-year='+ maxyear +'&order=date#filterForm'
urlDisney = 'https://es.flixable.com/disney-plus/?min-rating=' + rating +'&min-year='+ minyear +'&max-year='+ maxyear +'&order=date#filterForm'

def extraccionDatos(url,plataforma):
    #Abrir Firefox
    driver = webdriver.Firefox(executable_path="geckodriver.exe")
    driver.get(url)
    driver.maximize_window()

    #Desplazamiento pagina despacio
    time.sleep(1)
    iter=1
    while True:
        scrollHeight = driver.execute_script("return document.documentElement.scrollHeight")
        Height=250*iter
        driver.execute_script("window.scrollTo(0, " + str(Height) + ");")
        if Height > scrollHeight:
            print('Final de la pagina')
            break
        time.sleep(1)
        iter+=1

    #Leer html una vez se ha recorrido toda la página        
    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML')

    #Parsear con BeautifulSoup
    soup = BeautifulSoup(source, 'lxml')

    #Guardar clasificación imdb en lista
    an = soup.find_all('div', class_='card-description')
    annoMedia = list() #guarda los años
    for i in an:
        annoMedia.append(i.text)
    annoMedia = [x.replace('\n', '') for x in annoMedia] #limpiar espacios y \n
    annoMedia = [x.replace(' ', '') for x in annoMedia]
    anno = list()
    for word in annoMedia:
        anno.append(word[:4])
    listImdb = list() #guarda la nota imdb
    for word in annoMedia:
        listImdb.append(word[-6:])
    listImdb = [x.replace(' ', '') for x in listImdb]
    cambiar = [len(set(i)) == 1 for i in zip(anno,listImdb)] # compara las dos listas, si no tiene nota le pone valor NA
    i=0
    for word in cambiar:
        if word == True:
            listImdb[i] = 'NA'
        i += 1

    #Encontrar todos los enlaces a peliculas y series en la página
    titulosDivs = soup.findAll('div', attrs={'class' : 'card-header card-header-image'})
    titulosEnlace = list()
    for div in titulosDivs:
        titulosEnlace.append('https://es.flixable.com' + div.find('a')['href'])

    #print(titulosEnlace)

    #Recorrer los enlaces
    listTitPeli = list()
    listAnyo = list()
    listEdad = list()
    listDuracion = list()
    listGenero = list()
    listDirector = list()
    listActores = list()
    listPais = list()
    
     
    for url in titulosEnlace:
        t0 = time.time()
        response = requests.get(url)
        response_delay = time.time() - t0
        time.sleep(10 * response_delay)

        soup = BeautifulSoup(response.content, "html.parser")
    
        #Título de la película
        pel = soup.find('h1', class_='title text-left')
        listTitPeli.append(pel.text)
        #año
        anyo = soup.find('span', class_='mr-2')
        listAnyo.append(anyo.text)
        #edad recomendada
        edad = soup.find('span', class_='border border-secondary mr-2 px-1')
        listEdad.append(edad.text)
        #duracion
        duracion = soup.find_all('span')[11].text #Span en la posición 11(no tiene clase)
        listDuracion.append(duracion)
        #Generos
        try:
            genero = soup.find(text="Géneros:").findNext('span').text
            listGenero.append(genero)
        except:
            listGenero.append('NA')
        #Director
        try:
            director = soup.find(text="Director:").findNext('span').text
            listDirector.append(director)
        except:
            listDirector.append('NA')
        #Actores
        try:
            actores = soup.find(text="Actores:").findNext('span').text
            listActores.append(actores)
        except:
            listActores.append('NA')
        #País
        try:
            pais = soup.find(text="País de producción:").findNext('span').text
            listPais.append(pais)
        except:
            listPais.append('NA')



    #print(listTitPeli)
    #print(listAnyo)
    #print(listEdad)
    #print(listDuracion)
    #print(listGenero)
    #print(listDirector)
    #print(listActores)
    #print(listPais)
    #print(listImdb)

    driver.quit()
    
    #Extracción a dataframe
    df = pd.DataFrame({'Nombre': listTitPeli, 'Año': listAnyo, 'Edad': listEdad, 'Duración': listDuracion, 'Genero': listGenero, 'Director': listDirector, 'Actores': listActores, 'País': listPais, 'IMDb': listImdb, 'Plataforma': plataforma})
    print(df)
    if os.path.isfile('catalogo.csv') == False:
        df.to_csv('catalogo.csv', index=False, mode='a', encoding="utf-8")
    else:
        df.to_csv('catalogo.csv', header=False, index=False, mode='a', encoding="utf-8")


    

extraccionDatos(urlNetflix,"Netflix")
extraccionDatos(urlDisney,"Disney")

