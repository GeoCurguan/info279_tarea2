import pandas as pd
import os
import time
import googlemaps

GOOGLE_GEOCODING = os.getenv("GOOGLE_GEOCODING_KEY")
gmaps = googlemaps.Client(key=GOOGLE_GEOCODING)

df = pd.read_csv('test_21.csv')
# Geocoding
def geo(place: str) -> tuple[str, str]:
    geocode_result = gmaps.geocode(place)
    if geocode_result != []:
        lat = str(geocode_result[0]["geometry"]['location']['lat'])
        lng = str(geocode_result[0]["geometry"]['location']['lng'])
    else:
        return (None, None)
    return (lat, lng)

# Aplicar la función geo a la columna 'location' y dividir los resultados en dos columnas 'lat' y 'lng'
df[['lat', 'lng']] = df['location'].apply(lambda x: pd.Series(geo(x)))

# Guardar el DataFrame resultante en el mismo archivo CSV con las nuevas columnas
df.to_csv('test_21.csv', index=False)

print(df)