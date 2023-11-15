import numpy as np
import requests

places1 = np.array(['Cervecería', 'Parque', 'Plaza', 'Población', 
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

places2 = np.array(['Gimnasio', 'Club', 'Pueblo', 'Zona residencial', 'Condominio'
                    'Hogar', 'Cementerio','Salón de baile', 'Parroquia','Fábrica',
                    'Laboratorio', 'Estudio', 'Taller','Tienda','Bazar',
                    'Salón de belleza', 'Spa', 'Mercado nocturno' 'Taller mecánico'
                    'Granja','Rancho','Viñedo','Bodega','Campo de golf','Cancha de tenis',
                    'Piscina','Casino','Refugio','Hostal','Edificio histórico'
                    ,'Planta de energía','Aeródromo','Acantilado'])

def query(texto: str, api_key):
    url = 'https://places.googleapis.com/v1/places:searchText'
    data = {
        'textQuery': texto
    }
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel'
    }
    response = requests.post(url, json=data, headers=headers)
    return response
