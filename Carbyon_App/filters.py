import panel as pn
import time
import folium
import pandas as pd
from map import create_map
from color_map import Color_map


class Filters(pn.viewable.Viewer):
    def __init__(self, map, map_pane, **params):
        super().__init__(**params)
        
        # Existing map and map_pane passed in
        self.map = map
        self.map_pane = map_pane
 
        # Dropdowns
        self.overview_dropdown=pn.widgets.Select(
            name='Change overview',
            options=['€ / ton CO₂', 'kWh / ton'],
            value='€ / ton CO₂',
            styles={
                'width':'18%'
            }
            )
        
        self.machine_dropdown=pn.widgets.Select(
            name='Choose machine',
            options=['alpha1', 'alpha2'],
            value='alpha1',
            styles={
                'width':'18%'
            }
            )
        
        self.coordinates=pn.widgets.TextInput(
            name='Coordinates',
            placeholder="Latitude, Longitude",
            styles={
                'width':'21%'
            }
            )
        
        self.search_btn=pn.widgets.Button(
            name='SHOW ON MAP', icon='search',
            styles={
                'width':'10%',
            }
        )

        #Set the layout of the Row above the map with the filtering options and searchbar
        self._layout = pn.FlexBox(
            self.machine_dropdown,
            self.overview_dropdown,
            self.coordinates,
            self.search_btn,
            align_items="flex-end"

        )
        # Load the CSV file
        self.data = pd.read_csv('files/csv/alpha1.csv')
        # Handle dropdown selection
        self.overview_dropdown.param.watch(self.update_display_metric, 'value')
        

    def update_display_metric(self, event):
        # Get the selected value from the dropdown
        selected_metric = event.new.lower().replace(' / ', '_').replace(' ', '_')

        # Callback to update the map with the selected metric (euros or kWh)
        self.update_map_layers(selected_metric)

    def get_joined_data_for_metric(self, metric):
        """
        Fetch and join the necessary data for the selected metric.
        
        Depending on the selected metric ('euros_per_ton' or 'kwh_ton'),
        process the data and return the appropriate DataFrame for map layers.
        """
        # Print columns to help debug
        print(self.data.columns)
        # Example of joining data based on the metric
        if metric == 'euros_per_ton':
            # Assuming the 'CostsToCapture' column holds the cost data per ton
            # You might need to adjust this if you have additional transformations or joins
            joined_data = self.data[['geometry', 'description', 'GRIDCODE', 'CostsToCapture']].copy()
            
        elif metric == 'kwh_ton':
            # If the metric is related to energy efficiency (e.g., 'EnergyRequirements' per ton)
            joined_data = self.data[['geometry', 'description', 'GRIDCODE', 'EnergyRequirements']].copy()
            
        else:
            # If the metric doesn't match any known type, return an empty DataFrame
            return pd.DataFrame()

        # Additional transformations, if any, can be added here before returning the data
        return joined_data
    def update_map_layers(self, metric):
        """
        Update the map’s color or layer based on the selected metric.
        """
        # Remove previous layers if necessary
        for layer in list(self.map._children.values()):
            if isinstance(layer, folium.GeoJson):
                self.map.remove_child(layer)

        # Add new layers based on the selected metric
        joined_data = self.get_joined_data_for_metric(metric)
        
        climate_zones_fg = folium.FeatureGroup(name="Climate Zones", show=True)

        for _, row in joined_data.iterrows():
            geojson_feature = {
                'type': 'Feature',
                'geometry': row['geometry'].__geo_interface__,
                'properties': {
                    'description': row['description'],
                    'GRIDCODE': row['GRIDCODE'],
                    'CostsToCapture': row['CostsToCapture'],
                    'EnergyRequirements': row['EnergyRequirements']
                }
            }

            fields = ['description']
            aliases = ['Climate Zone:']
            if metric == 'euros_per_ton':
                fields.append('CostsToCapture')
                aliases.append('Cost per ton (€):')
            elif metric == 'kwh_ton':
                fields.append('EnergyRequirements')
                aliases.append('Energy per ton (kWh):')

            folium.GeoJson(
                geojson_feature,
                style_function=lambda x, color=row['color']: {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 0.5,
                    'fillOpacity': 0.6,
                },
                tooltip=folium.GeoJsonTooltip(
                    fields=fields,
                    aliases=aliases,
                    localize=True,
                    sticky=True,
                    labels=True,
                    style="font-size: 12px; color: black;"
                )
            ).add_to(climate_zones_fg)

        climate_zones_fg.add_to(self.map)
        folium.LayerControl().add_to(self.map)

        # Refresh map HTML and layout
        self.map_pane.object = self.map._repr_html_()
        self._layout[0] = self.map_pane

    def Search(self, add_marker_callback, update_display_callback):
        def handle_click(event):
            # Use next tick callback to ensure coordinates value is updated
            coordinates = self.coordinates.value.strip()
            print(f"Coordinates entered: '{coordinates}'")  # Debug log to ensure coordinates are being read

            # Check if coordinates are empty
            if not coordinates:
                print("No coordinates provided. Please enter valid coordinates.")
                update_display_callback({"message": "No coordinates provided. Please enter valid coordinates."})
                return

            # Ensure the coordinates are in valid format (latitude, longitude)
            if ',' not in coordinates:
                print("Invalid format. Coordinates should be in 'latitude, longitude' format.")
                update_display_callback({"message": "Invalid format. Coordinates should be in 'latitude, longitude' format."})
                return

            # Delay the processing using add_next_tick_callback to handle async UI updates
            pn.state.curdoc.add_next_tick_callback(lambda: self.process_coordinates(coordinates, add_marker_callback, update_display_callback))

        # Connect the button click event to the handler function
        self.search_btn.on_click(handle_click)

    def process_coordinates(self, coordinates, add_marker_callback, update_display_callback):
        try:
            # Parse the coordinates
            lat, lon = map(float, coordinates.split(','))
            print(f"Searching for: {lat}, {lon}")

            # Check for coordinates in the CSV
            match = self.data[(self.data['Lat'] == lat) & (self.data['Long'] == lon)]

            if not match.empty:
                location_details = match.iloc[0].to_dict()
                update_display_callback(location_details)
                add_marker_callback((lat, lon))
            else:
                # Coordinates not found in the dataset
                update_display_callback({"message": "Coordinates not found in the dataset."})
                add_marker_callback((lat, lon))

        except ValueError:
            # Handle invalid coordinate format
            print("Invalid coordinates format. Ensure the format is 'latitude, longitude'.")
            update_display_callback({"message": "Invalid coordinates format. Ensure the format is 'latitude, longitude'."})


       

    # Expose the layout for rendering
    def __panel__(self):
        return self._layout