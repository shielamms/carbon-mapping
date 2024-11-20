from streamlit_folium import st_folium
import folium
import json
import streamlit as st

st.set_page_config(layout="wide")


def create_map(data):
    map = folium.Map(tiles="OpenStreetMap", location=[31.8,0], zoom_start=2.2)

    for region in data:
        highest_source = region['highest_source']
        if highest_source in ('gas', 'coal', 'oil', 'battery discharge'):
            colour = 'red'
        elif highest_source == 'nuclear':
            colour = 'orange'
        elif highest_source in ('hydro', 'biomass', 'solar', 'wind', 'geothermal', 'hydro discharge'):
            colour = 'green'
        else:
            colour = 'gray'

        energy_pct = round(float(region[highest_source]), 2)

        text = f'{region["region"]} ({region["name"]}): {highest_source} ({energy_pct}%)'
        
        marker = folium.Marker(
            location=(region['lat'], region['lon']),
            popup=text,
            icon=folium.Icon(color=colour)
        )
    
        map.add_child(marker)

    return map


if __name__ == '__main__':
    data_filename = 'datecenter_power_breakdown.json'

    with open(data_filename, 'r') as f:
        print(f'Reading file {data_filename}...')
        data = json.load(f)
    
    folium_map = create_map(data)
    st_data = st_folium(folium_map, width=1065)
    st.write(st_data)
