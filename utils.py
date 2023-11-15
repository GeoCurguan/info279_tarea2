import numpy as np
import requests

places = np.array(['Cervecería', 'Parque', 'Plaza', 'Población', 
                   'Villa', 'Pasaje', 'Sector', 'Hospital', 'Escuela', 
                   'Colegio', 'Universidad', 'Cine', 'Puente', 
                   'Avenida', 'Calle', 'Barrio', 'Estación', 'Mercado', 
                   'Biblioteca', 'Centro comercial', 'Terminal', 
                   'Jardín', 'Museo', 'Teatro', 'Galería', 'Estadio', 
                   'Café', 'Restaurante', 'Iglesia', 'Oficina', 
                   'Embajada', 'Estación de policía', 'Estación de bomberos', 
                   'Estación de tren', 'Estación de autobuses', 'Aeropuerto', 
                   'Puerto', 'Playa', 'Montaña', 'Río', 'Lago', 'Bosque', 
                   'Acuario', 'Mirador', 'Monumento', 'Torre', 
                   'Faro', 'Camino', 'Sendero'])


def query(texto: str):
    url = 'https://places.googleapis.com/v1/places:searchText'
    data = {
        'textQuery': texto
    }
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': 'AIzaSyAjbtkLeCtZfQWp5zOyIGwmrBSpCtq9Lps',
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel'
    }
    response = requests.post(url, json=data, headers=headers)
    return response
