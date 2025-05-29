import os
import folium
import geopandas as gpd
import pandas as pd
import panel as pn
from legend import climate_map_legend
from color_map import Color_map
from performance import performance_filter
import shapely
from shapely.geometry import Point

def create_map(koppen_giger_data_path: str, color_map, display_metric='euros_per_ton'):
    # Load the Köppen-Geiger climate classification shapefile into a GeoDataFrame
    koppen_giger_data = gpd.read_file(koppen_giger_data_path)

    # Load the CSV containing the additional data (CostsToCapture and EnergyRequirements)
    additional_data = pd.read_csv('files/csv/alpha1.csv')

    # Create a GeoDataFrame for the additional data with Lat, Long columns
    additional_data['geometry'] = additional_data.apply(
        lambda row: Point(row['Long'], row['Lat']), axis=1
    )
    additional_data_gdf = gpd.GeoDataFrame(additional_data, geometry='geometry', crs="EPSG:4326")

    # Ensure the shapefile is in the same CRS as the additional data (EPSG:4326)
    koppen_giger_data = koppen_giger_data.to_crs(epsg=4326)

    # Perform a spatial join: Find which climate zone contains each point from the CSV
    joined_data = gpd.sjoin(koppen_giger_data, additional_data_gdf, how="left", predicate='intersects')

    # Add color and description columns based on GRIDCODE (mapping GRIDCODE to colors)
    joined_data['color'] = joined_data['GRIDCODE'].map(lambda x: color_map.get(x, ('gray', 'Unknown'))[0])
    joined_data['description'] = joined_data['GRIDCODE'].map(lambda x: color_map.get(x, ('gray', 'Unknown'))[1])

    # Create a Folium Map centered on a given location
    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")

    # FeatureGroup for the climate zones
    climate_zones_fg = folium.FeatureGroup(name="Climate Zones", show=True)

    # Add each feature to the FeatureGroup with corresponding color and tooltip
    for _, row in joined_data.iterrows():
        geojson_feature = {
            'type': 'Feature',
            'geometry': row['geometry'].__geo_interface__,  # Using __geo_interface__ to get proper GeoJSON structure
            'properties': {
                'description': row['description'],
                'GRIDCODE': row['GRIDCODE'],
                'CostsToCapture': row['CostsToCapture'],
                'EnergyRequirements': row['EnergyRequirements']
            }
        }

        # Initialize fields and aliases with the basic fields
        fields = ['description']
        aliases = ['Climate Zone:']
        # Conditionally append the selected display metric field and alias
        if display_metric == 'euros_per_ton':
            fields.append('CostsToCapture')
            aliases.append('Cost per ton (€):')
        elif display_metric == 'kwh_ton':
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

    # Add the climate zones FeatureGroup to the map
    climate_zones_fg.add_to(m)

    # Add LayerControl
    folium.LayerControl().add_to(m)

    # Callback function for the legend (from legend.py)
    legend = climate_map_legend()

    # Add the legend to the map
    m.get_root().html.add_child(folium.Element(legend))

    # Return the HTML representation of the map
    return m


class ClimateMap(pn.viewable.Viewer):
    def __init__(self, koppen_giger_data_path: str, color_map=None, map=None, map_pane=None, **params):
        super().__init__(**params)
        self.path = os.path.abspath(koppen_giger_data_path)
        self.original_color_map = color_map if color_map else Color_map()  # Ensure color_map is initialized
        self.color_map = self.original_color_map  # Initially set to the original color map
        # If map and map_pane are provided, use them; otherwise, create new ones
        if map and map_pane:
            self.map = map
            self.map_pane = map_pane
        else:
            # Create the map and map_pane if they are not passed in
            self.map = create_map(self.path, self.color_map)
            self.map_pane = pn.pane.HTML(self.map._repr_html_())

        self._layout = pn.Column(self.map_pane)
        # Load the shapefile and ensure that 'description' is added to the DataFrame
        self.koppen_giger_data = gpd.read_file(self.path)
        # Add color and description columns based on GRIDCODE
        self.koppen_giger_data['color'] = self.koppen_giger_data['GRIDCODE'].map(
            lambda x: self.color_map.get(x, ('gray', 'Unknown'))[0]
        )
        self.koppen_giger_data['description'] = self.koppen_giger_data['GRIDCODE'].map(
            lambda x: self.color_map.get(x, ('gray', 'Unknown'))[1]
        )
        print(self.koppen_giger_data.columns)  # Debugging step to confirm that 'description' exists
         
    
    def get_climate_zone_for_coordinates(self, lat, lon):
        """
        Given latitude and longitude, find the corresponding climate zone.
        Returns the description of the climate zone and its GRIDCODE.
        """
        # Debug: Print columns to ensure 'description' exists
        print(self.koppen_giger_data.columns)
        # Create a Point object for the coordinates
        point = Point(lon, lat)
        
        # Loop through each polygon in the shapefile
        for _, row in self.koppen_giger_data.iterrows():
            if row['geometry'].contains(point):  # Check if the point is inside the polygon
                # If found, return the corresponding climate zone description and GRIDCODE
                return {
                    'description': row['description'],
                    'GRIDCODE': row['GRIDCODE']
                }

        # If no matching zone is found, return None
        return None
    ### DEFINING FUNCTIONS FOR ACTIONS ###
    def add_marker(self, coordinates, update_display_callback=None):
        try:
            print(f"Received coordinates: {coordinates}") 
            # Unpack the tuple directly
            if isinstance(coordinates, tuple):
                lat, lon = coordinates
            else:
            # Fallback for string input
                lat, lon = map(float, coordinates.split(','))

            print(f"Parsed coordinates: {lat}, {lon}")  
            # Add the marker details to the list

            # Find the climate zone for the coordinates
            climate_info = self.get_climate_zone_for_coordinates(lat, lon)

            if climate_info:
                climate_description = climate_info['description']
                gridcode = climate_info['GRIDCODE']
                print(f"Climate Zone: {climate_description} (GRIDCODE: {gridcode})")
                
                # Add a marker with climate zone information
                popup_html = f"""
                    <p>Marker at <br> ({lat}, {lon})</p>
                    <p><strong>Climate Zone:</strong> {climate_description} (GRIDCODE: {gridcode})</p>
                    <button onclick="alert('More details for location: {lat}, {lon}')">More Details</button>
                """
                folium.Marker(location=(lat, lon), popup=folium.Popup(popup_html, max_width=300)).add_to(self.map)
            else:
                print("Coordinates are outside the defined climate zones.")
                popup_html = f"""
                    <p>Marker at <br> ({lat}, {lon})</p>
                    <p><strong>Climate Zone:</strong> Not Found</p>
                """
                folium.Marker(location=(lat, lon), popup=folium.Popup(popup_html, max_width=300)).add_to(self.map)
            
            # Refresh map HTML
            self.map_pane.object = self.map._repr_html_()
            self._layout[0] = self.map_pane  # Refresh the layout with updated map
            print("Map HTML updated")  
            if update_display_callback:
                update_display_callback(f"{lat}, {lon}")
        except ValueError:
            print("Invalid coordinates. Ensure the format is 'latitude, longitude'")
    

    def apply_performance_filter(self, selected_performance):
        """
        Apply a performance filter to the map based on the selected performance level.
        """
        if selected_performance == 'Choose performance':
            # If the default option is selected, reset to the full color map
            self.reset_to_full_color_map()
            
        else:
            # Call the performance function to filter the color map
            filtered_color_map = performance_filter(self.color_map, selected_performance)
            
            # Update the map with the filtered color map
            self.update_map_colors(filtered_color_map)

    def update_map_colors(self, color_map):
        """
        Update the map with a new color map.
        """

        # Update the color map
        self.color_map = color_map
        
        # Recreate the map with the new color map
        self.map = create_map(self.path, self.color_map)  # Recreate the map with the new color map
        
        # Explicitly refresh the HTML pane with the updated map
        self.map_pane.object = self.map._repr_html_()  # Update the HTML content
        
        # Recreate the layout with the updated map pane
        self._layout[0] = self.map_pane  # Update the layout with the new pane

    def reset_to_full_color_map(self):
        """
        Reset the map to its original, full-color state.
        """
        
        self.color_map = self.original_color_map  # Reset to the original color map
        self.update_map_colors(self.color_map)  # Update the map with the full color map

    
    def __panel__(self):
        return self._layout
