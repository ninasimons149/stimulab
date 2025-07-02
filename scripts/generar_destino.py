import requests
import time
import json
from pathlib import Path

def fetch_libros_destino(page=1):
    url = f'https://openlibrary.org/search.json'
    params = {
        'publisher': 'destino',
        'limit': 100,
        'page': page
    }
    resp = requests.get(url, params=params)
    return resp.json().get('docs', [])

def fetch_sinopsis(work_key):
    try:
        resp = requests.get(f'https://openlibrary.org{work_key}.json')
        data = resp.json()
        desc = data.get('description')
        if isinstance(desc, dict):
            return desc.get('value')
        elif isinstance(desc, str):
            return desc
    except:
        return None

def portada_url(cover_i):
    return f'https://covers.openlibrary.org/b/id/{cover_i}-L.jpg' if cover_i else None

def generar_json(archivo_salida='destino_libros.json', total=500):
    libros = []
    page = 1
    while len(libros) < total:
        print(f'⏳ Consultando página {page}...')
        docs = fetch_libros_destino(page)
        if not docs:
            break
        for d in docs:
            año = d.get('first_publish_year')
            if año and año < 2010:
                continue
            libro = {
                'titulo': d.get('title'),
                'autor': d.get('author_name', [None])[0],
                'anio_publicacion': año,
                'ISBN': d.get('isbn', [None])[0],
                'sinopsis': fetch_sinopsis(d.get('key')),
                'portada': portada_url(d.get('cover_i'))
            }
            libros.append(libro)
            time.sleep(0.1)
            if len(libros) >= total:
                break
        page += 1

    Path("data").mkdir(parents=True, exist_ok=True)
    with open('data/' + archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(libros, f, ensure_ascii=False, indent=2)

    print(f'✅ Archivo generado con {len(libros)} libros.')

if __name__ == '__main__':
    generar_json()