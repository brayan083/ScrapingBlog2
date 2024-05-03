from urllib.parse import urlparse
from time import sleep
from random import randint
from requests.exceptions import ProxyError, ConnectionError
from bs4 import BeautifulSoup
import requests

def scrape_website(url):
    try:
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        
        # Realizar la solicitud GET al sitio web con proxies configurados
        response = requests.get(url, headers=headers)
        html = response.content
        # print(response)
        
        parsed_url = urlparse(url)
        dominio = f"{parsed_url.scheme}://{parsed_url.netloc}"
        # print(dominio)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            
            # Parsear el contenido HTML de la página web
            soup = BeautifulSoup(html, 'html.parser')
            
            # Obtener el título de la página
            page_title = soup.title.string if soup.title else None
            
            # Obtener la meta descripción de la página
            meta_description_tag = soup.find('meta', attrs={'name':'description'}) or \
                                    soup.find('meta', attrs={'name':'Description'}) or \
                                    soup.find('meta', attrs={'property':'og:description'})
            meta_description = meta_description_tag['content'] if meta_description_tag else None
            
            # Obtener todas las etiquetas h1
            h1_tags = soup.find_all('h1')
            h1_texts = [tag.get_text().strip().replace('\n', '') for tag in h1_tags]
            
            # Obtener todas las etiquetas h2
            h2_tags = soup.find_all('h2')
            h2_texts = [tag.get_text().strip().replace('\n', '') for tag in h2_tags]

            # Obtener todas las etiquetas h3
            h3_tags = soup.find_all('h3')
            h3_texts = [tag.get_text().strip().replace('\n', '') for tag in h3_tags]
            
            # Esto es para obtener todos los links a los que se puede navegar desde esta url
            links = []
            for link in soup.find_all('a'):
                if link.get('href') != None:
                    links.append(link.get('href'))
            
            links_limpio = [f"{dominio}{elemento}" if elemento.startswith('/') else elemento for elemento in links if elemento[0] in ['/', 'h']]
            # print(links_limpio)
            
            # Eliminar todos los enlaces <a> del HTML
            for a_tag in soup.find_all('a'):
                a_tag.decompose()
                
            # Eliminar el pie de página
            for footer_tag in soup.find_all('footer'):
                footer_tag.decompose()

            # También puedes buscar divs con la clase o id "footer"
            for footer_div in soup.find_all('div', {'class': 'footer'}):
                footer_div.decompose()
            for footer_div in soup.find_all('div', {'id': 'footer'}):
                footer_div.decompose()
                
            page_text = soup.get_text().split("\n")
            new_page_text = []
            for i in page_text:
                if i != '' and len(i) > 50:
                    new_page_text.append(i.strip())
            
            new_page_text = ' '.join(new_page_text)
            # print(new_page_text)
            
            return page_title, meta_description, h1_texts, h2_texts, h3_texts, links_limpio, new_page_text

        else:
            # Si la solicitud no fue exitosa, imprimir un mensaje de error
            return f"Error al obtener la página: {response.status_code}"
    except ProxyError as e:
        return f"Error de proxy al procesar la URL: {str(e)}"
    except ConnectionError as e:
        return f"Error de conexión al procesar la URL: {str(e)}"
    except Exception as e:
        return f"Error al procesar la URL: {str(e)}"