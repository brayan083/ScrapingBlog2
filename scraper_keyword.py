import requests
from bs4 import BeautifulSoup

def obtener_urls_posicionadas(keyword):
    # Construir la URL de búsqueda de Google
    url = f"https://www.google.com/search?q={keyword}"

    # Definir los headers de la solicitud
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Enviar la solicitud HTTP y obtener la página de resultados de búsqueda
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parsear la página de resultados con BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        print('soy soup: ',soup)
        

        
    else:
        print("Error al obtener la página de resultados de búsqueda.")
        return None


res = obtener_urls_posicionadas("cajas")
print('soy res: ',res)

# Ejemplo de uso
# keyword = input("Ingresa una palabra clave: ")
# urls_posicionadas = obtener_urls_posicionadas(keyword)
# print(urls_posicionadas)

# if urls_posicionadas:
#     print("Las URLs mejor posicionadas para la palabra clave '{}' son:".format(keyword))
#     for i, (titulo, url) in enumerate(urls_posicionadas, start=1):
#         print(f"{i}. Título: {titulo}")
#         print(f"   URL: {url}\n")
# else:
#     print("No se encontraron resultados para la palabra clave proporcionada.")
