## Mapping the Carbon Emissions of AWS Datacentres (WIP)

This project aims to map AWS Datacentres and identify the main source of electricity of each area by looking at its power consumption breakdown at a particular point in time. The power data is provided for free by [electricitymaps.org](https://www.electricitymaps.org/). The map application is written in Python.

### Current Setup

#### Prerequisites
- Python 3.10.
- An ElectricityMaps API key - request one from the [API website](https://www.electricitymaps.com/get-our-data)

#### Dependencies

To install the project dependencies, run:

```
pip install -r requirements.txt
```

Then set the `ELECTRICITY_MAPS_API_KEY` environment variable with your ElectricityMaps API Key:

```
export ELECTRICITY_MAPS_API_KEY=<your API key>
```

#### Running the application

Run the `update.py` script first to update the power consumption data with the latest from the API:

```
python update.py
```

The app runs in Streamlit, so you'll need the Streamlit SDK to view the map in your browser:

```
streamlit run app.py
```


### Work in Progress..

- The app is currently served in Streamlit, which has its own limitations when rendering folium maps (it keeps reloading the page on every click)
- You'll need to run the `update.py` manually to update the data. This can be automated.
- The CI is just skeleton for now.
