import folium
import pandas
data=pandas.read_csv('/Users/eli/Documents/Data_science/python3/2_webmap_application/app2-web-map/Volcanoes_USA.txt')
lat=list(data['LAT'])
lon=list(data['LON'])
ele=list(data['ELEV'])
vol_name=list(data['NAME'])

map=folium.Map(location=[39.659542, -109.288048],zoom_start=4, tiles='Mapbox Bright')

fgv=folium.FeatureGroup(name='Volcanos')


def color_producer(elevation):
    if elevation<1000:
        return 'green'
    elif 1000<=elevation<3000:
        return 'orange'
    else:
        return 'red'

for i,j,elev,name_v in zip(lat, lon,ele,vol_name):
    popup = folium.Popup('Elevation of '+name_v+' is: '+ str(elev)+' meters', parse_html=True)
    #fg.add_child(folium.Marker(location=[i,j],popup=popup,icon=folium.Icon(icon='cloud',color=color_producer(elev))))
    fgv.add_child(folium.CircleMarker(location=[i,j],popup=popup,radius=5,color=color_producer(elev),fill_opacity=0.7,fill=True))

# adding poligons
fgp=folium.FeatureGroup(name='Population')

fgp.add_child(folium.GeoJson(data=(open('/Users/eli/Documents/Data_science/python3/2_webmap_application/app2-web-map/world.json',encoding='utf-8-sig').read()),style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005']<10000000 else 'orange' if 10000000<=x['properties']['POP2005']<20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save('Map1.html')
