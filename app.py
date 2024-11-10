from dotenv import load_dotenv, find_dotenv
from streamlit_folium import st_folium
from typing import Dict
import folium
import json
import os
import requests
import streamlit as st

st.set_page_config(layout="wide")


def load_emaps_api_key():
    load_dotenv(find_dotenv())
    api_key = os.getenv('ELECTRICITY_MAPS_API_KEY')
    if not api_key:
        print('No API key found in environment')
    else:
        return api_key


def get_latest_power_breakdown(coordinates: Dict[str, float]):
    assert 'lat' in coordinates
    assert 'lon' in coordinates
    
    url = f"https://api.electricitymap.org/v3/power-breakdown/latest?lat={coordinates['lat']}&lon={coordinates['lon']}"
    request = requests.get(url, headers={'auth-token': load_emaps_api_key()})
    power_breakdown = json.loads(request.content)
    
    total_consumption = power_breakdown['powerConsumptionTotal']
    power_consumption_pct = {
        k:v/total_consumption*100
        for k,v
        in power_breakdown['powerConsumptionBreakdown'].items()
    }

    return power_consumption_pct


def process_datacenters():
    aws_regions = []

    with open('aws_datacenters', 'r') as f:
        data = f.readlines()

    for region in data:
        region = region.replace('\n', '').strip()
        parts = region.split(';')
        if len(parts) != 4:
            print('Unable to parse line', parts, 'Skipping...')
            continue
        aws_regions.append({
            'region': parts[0],
            'name': parts[1],
            'lat': parts[2],
            'lon': parts[3],
        })

    return aws_regions


def make_energy_breakdown_list(aws_regions):
    data = []

    for region in aws_regions:
        power_breakdown = get_latest_power_breakdown(region)
    
        # Determine highest contributing energy source
        highest_source = max(power_breakdown, key=power_breakdown.get)

        region.update(power_breakdown)
        region['highest_source'] = highest_source
        data.append(region)

    return data


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


datacenters = process_datacenters()
data = make_energy_breakdown_list(datacenters)
folium_map = create_map(data)

st_data = st_folium(folium_map, width=1065)
st.write(st_data)
