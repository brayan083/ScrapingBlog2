from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')


from scraper_website import scrape_website
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
        
        result_dict = {
        'title': result[0],
        'description': result[1],
        'h1': result[2],
        'h2': result[3],
        'h3': result[4],
        'links': result[5],
        'text': result[6]
        }

        # Devolver el resultado como JSON
        return jsonify({"result":result_dict})
    else:
        return jsonify({'error': 'La clave "url" no se proporcionó en el cuerpo JSON'}, 400)

from scraper_keyword import obtener_hrefs
@app.route('/scrape_keyword', methods=['POST'])
def scrape_keyword():
    data = request.json
    
    if 'keyword' in data:
        keyword = data['keyword']
        # print(keyword)
        
        hrefs = obtener_hrefs(keyword)
        # print(hrefs)
        
        return jsonify({"result":hrefs})
    

@app.route('/hello/<name>')
def name(name):
    print(name)
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run()
