from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

def obtener_hrefs(keyword):
    
    new_keyword = keyword.replace(' ', '+')
    
    url = f"https://www.google.com/search?q={new_keyword}"
    # Configurar Selenium para que funcione en modo headless
    opciones = Options()
    # opciones.headless = True
    opciones.add_argument("--headless")
    navegador = webdriver.Firefox(options=opciones)

    # Obtener el HTML de la página
    navegador.get(url)
    html = navegador.page_source
    navegador.quit()

    # Analizar el HTML con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # la etiqueta que tiene esta clase contiene los hrefs con las url de pago, las que dice "Anuncio" o "Publicidad" o "Patrocinado"
    clase1 = 'Pm5mre'
    
    elementos1 = soup.find_all(class_=clase1)
    
    UrlsAnuncios = []
    for elemento in elementos1:
        for a in elemento.find_all('a'):
            url = a.get('href')
            if url not in UrlsAnuncios and url is not None and url.startswith(('http://', 'https://')) and len(url) <= 75:
                UrlsAnuncios.append(url)
    
    
    # la etiqueta que tiene esta clase contiene los hrefs con las url Organicas
    clase = 'dURPMd'

    # Buscar los elementos con la clase especificada
    elementos = soup.find_all(class_=clase)

    # Extraer los hrefs únicos y ordenados de los elementos
    UrlsOrganicas = []
    for elemento in elementos:
        for a in elemento.find_all('a'):
            url = a.get('href')
            # este if gigante valida que la url no esté en la lista, que no sea None, que empiece con http o https y que tenga una longitud menor a 75 
            if url not in UrlsOrganicas and url is not None and url.startswith(('http://', 'https://')) and len(url) <= 100:
                UrlsOrganicas.append(url)

    return {"urls Anuncios":UrlsAnuncios, "Urls Organicas": UrlsOrganicas}

# hrefs = obtener_hrefs('carton cajas')
# print(hrefs)

# # Imprimir los hrefs linea por linea
# for href in hrefs:
#     print(href)