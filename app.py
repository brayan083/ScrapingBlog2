from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
from requests.exceptions import ProxyError, ConnectionError
from bs4 import BeautifulSoup
from flask_cors import CORS
import os

load_dotenv()


app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

def scrape_website(url):
    try:
        
        # Realizar la solicitud GET al sitio web con proxies configurados
        response = requests.get(url)
        print(response)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Parsear el contenido HTML de la página web
            soup = BeautifulSoup(response.content, 'html.parser')

            # Buscar el contenedor principal que contiene el contenido del blog
            main_content = soup.find("article")

            # Si no se encuentra el contenedor principal, intentar buscar por otras etiquetas comunes
            if not main_content:
                main_content = soup.find("div", {"id": "content"})
            if not main_content:
                main_content = soup.find("div", {"class": "entry-content"})
            if not main_content:
                return "No se encontró el contenido principal en la página."

            # Obtener todo el texto dentro del elemento <article>
            article_text = main_content.get_text(separator='\n', strip=True)
            # print(article_text)
            return article_text
        else:
            # Si la solicitud no fue exitosa, imprimir un mensaje de error
            return f"Error al obtener la página: {response.status_code}"
    except ProxyError as e:
        return f"Error de proxy al procesar la URL: {str(e)}"
    except ConnectionError as e:
        return f"Error de conexión al procesar la URL: {str(e)}"
    except Exception as e:
        return f"Error al procesar la URL: {str(e)}"

# Definir una ruta para tu API
@app.route('/scrape', methods=['POST'])
def scrape():
    
    # Obtener los datos JSON del cuerpo de la solicitud
    data = request.json
    print(data)

    # Verificar si se proporciona la clave 'url' en el JSON
    if 'url' in data:
        # Obtener la URL del JSON
        url = data['url']
        print(url)

        # Llamar a la función scrape_website con la URL
        result = scrape_website(url)

        # Devolver el resultado como JSON
        return jsonify({"result":result})
    else:
        return jsonify({'error': 'La clave "url" no se proporcionó en el cuerpo JSON'}, 400)

@app.route('/hello/<name>')
def name(name):
    print(name)
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run()
