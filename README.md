# Práctica 1: Web scraping

## Descripción

WebScrappingFlixable es un script hecho en Python por alumnos de la Universitat Oberta de Catalunya (UOC) para la asignatura de  _Tipología y ciclo de vida de los datos_  del Máster en Ciencia de Datos. En el, se aplican técnicas de _web scraping_ con el objetivo de extraer datos de películas y series de la web _flixable_ y con ello producir un _dataset_.

## Miembros del equipo

La práctica ha sido elaborada en conjunto por **Nil Busquets Aran** y **Adrián López Ibáñez**.

## Instalación

Para poder ejecutar este script es necesario instalar primero las siguientes bibliotecas:

```
pip install beautifulsoup4
pip install selenium
pip install requests
pip install pandas
pip install lxml
```
Asimismo, es necesario introducir en la misma carpeta que el proyecto el programa [geckodriver ]( https://github.com/mozilla/geckodriver) en su versión compatible con su dispositivo y tener Mozilla Firefox instalado.

## Uso

El script se ejecuta de la siguiente manera:
```
python WebScrappingFlixable.py
```
En la consola se debe responder a las preguntas:
```
¿Año comienzo de los datos?
¿Año fin de los datos?
¿puntuación mínima en imdb?
```
Se tiene que responder de la siguiente forma:
- Cuatro dígitos con el año de inicio de los datos
- Cuatro dígitos con el año de fin de los datos
- Número del 0 al 10 con la puntuación mínima en IMDb

Con estos datos se extrae los siguientes datos de Netflix y Disney+ en España:
- Título de la película o serie
- Año de publicación de la película o última temporada de la serie
- Edad recomendada
- Duración en minutos de la película o temporadas de la serie
- Genero
- Director
- Actores
- País de producción
- Nota Imdb
- Plataforma
