import requests
import os
import json
import folium
import pandas as pd

#creates new Constitution objects with country name and constitution text
def add(request):

    country_data_csv = open(os.path.join(settings.BASE_DIR, 'conex/static/conex/countr_ids.csv'))
    country_data = pd.read_csv(country_data_csv)

    for i in range(len(country_data)):
        country_id = country_data['country_id'][i]
        url = 'https://www.constituteproject.org/service/html?cons_id='+country_id+'&lang=en'
        response = requests.get(url)
        data = response.json()
        html = data['html']
        # country = Constitution.objects.get(pk=(i+1))
        country = Constitution()
        country.country=country_data['country'][i]
        country.constitution_text=html
        country.write_date=country_data['year_enacted'][i]
        country.save()
    
    return render(request, 'conex/add.html')

#create Folium map with given data input
def map(request):
    
    map = folium.Map(location=[0, 0], zoom_start=2, scrollWheelZoom=False, tiles='stamenwatercolor', max_bounds=True, min_lon=-180, max_lon=180, min_zoom=2)
    con_data_csv = open(os.path.join(settings.BASE_DIR, 'conex/static/conex/enacted_date_data.csv'))
    world_geo = os.path.join(settings.BASE_DIR, 'conex/static/conex/world_geo.json')
    world_geojson = json.load(open(world_geo))
    con_data = pd.read_csv(con_data_csv)
    bins=[1750, 1800, 1850, 1900, 1930, 1975, 2000, 2023]
    


    style_function = "font-size: 15px; font-weight: bold"

    for i in range(len(world_geojson['features'])):
        for x in range(len(con_data['year_enacted'])):
            if(world_geojson['features'][i]['properties']['name'] == con_data['country'][x]):
                world_geojson['features'][i]['properties']['tooltip'] = str(con_data['country'][x]) + " " + str(con_data['year_enacted'][x])[:-2]


    choro = folium.Choropleth(
        geo_data=world_geojson,
        name="choropleth",
        data=con_data,
        columns=["country", "year_enacted"],
        key_on="feature.properties.name",
        fill_color="RdYlGn",
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name="Year Enacted",
        bins=bins,
        highlight=True
    )

    choro.geojson.add_child(
        folium.features.GeoJsonTooltip(['tooltip'], style=style_function, labels=False))

    choro.add_to(map)
    map.save("folium_map.html")

    return render(request, 'conex/map.html')