import panel as pn
from map import ClimateMap
from filters import Filters
from performance import performance_filter
from color_map import Color_map

### STYLING ###

# Padding for the overall content
padding_style = {
    'padding': '20px',  
}

# Define individual styles for ID and Date
id_style = {
    'padding': '0',
    'margin': '0 !important',
    'line-height': '0',
    'height': '1vh',
    'position':'relative',
    'left':'0',
    'top':'0',
}

title = {
    'font-size': '1.5em',
    'margin': 'auto'
}
margin = {
    'margin-top': '2vh'
}
location_details={
    'height':'4vh',
    'font-size':'1.2em',
    'font-weight':'bold'
}


class Overview(pn.viewable.Viewer):
    def __init__(self):
        super().__init__()
        self._map=ClimateMap('files/2026-2050_A1FI_GIS/2026-2050-A1FI.shp')
        self._filters = Filters(map=self._map.map, map_pane=self._map.map_pane)
        self.color_map=Color_map()
        self._searchBtn = self._filters.Search(self._map.add_marker, self.update_display_input)
        self.displayInput=pn.pane.Markdown() 
        self.slider=pn.widgets.RangeSlider(name='Costs (€/ton)', format='0.0a', start=270, end=600)
        self.slider.styles = margin
        self.performance_dropdown=pn.widgets.Select(
            name='Performance',
            options=['Choose performance',
                'Best CO₂ Capture: Cost €277-€453/ton',
                'Good CO₂ Capture: Cost €281-€496/ton',
                'Moderate CO₂ Capture: Cost €327-€501/ton',
                'Worst CO₂ Capture: Cost €357-€568/ton'
                ],
            value='Choose performance'
            )
        
        # Attach callback to update map on dropdown selection
        self.performance_dropdown.param.watch(self.update_map, 'value')
        # Watch the overview_dropdown for changes
        self._filters.overview_dropdown.param.watch(self.switch_dropdown_options, 'value')
        self._filters.overview_dropdown.param.watch(self.update_slider, 'value')

        ## SETTING THE PAGE LAYOUT ###

        # Creating a layout with the content, including the padding around the whole content
        self._layout = pn.Column(

            pn.Row(
                pn.pane.Markdown("# Location and Weather Sensitivity", styles=title),
                sizing_mode='stretch_width',  
                align='center',
                styles={'text-align': 'center'}  
            ),

            pn.Column(
                pn.pane.Markdown("**ID:** ", styles=id_style),  
                pn.pane.Markdown("**Date:** ", styles=id_style),
                styles={'width': 'fit-content', 'height': '1vh', 'margin-bottom':'50px',}
            ),

            pn.Row(
                self._filters,
            ),

            pn.Row(
                self._map,
                pn.Column(
                    self.performance_dropdown,
                    self.slider,
                    pn.pane.Markdown("**Location Details:** ", styles=location_details),
                    self.displayInput
                    ),
                styles={'display':'grid', 'grid-template-columns':'75% 25%'}
            ),
            styles=padding_style,  # Apply padding around the whole content
        )

    ### CALLBACK FUNCTIONS FOR ACTIONS ###    
    def update_map(self, event):
        """
        Callback to update the map based on the selected performance filter.
        """
        selected_performance = event.new  # Get the selected performance from dropdown
        if selected_performance == 'Choose performance':
            # If the default option is selected, reset to the original color map
            self._map.reset_to_full_color_map()
        else:
            # Filter the color map based on performance
            updated_color_map = performance_filter(self.color_map, selected_performance)
            
            # Update the ClimateMap colors dynamically
            self._map.update_map_colors(updated_color_map)  # Call existing method in ClimateMap
    
    def update_display_input(self, location_details):
        """
        Update the display with location details or a not found message.
        """
        if "message" in location_details:
            self.displayInput.object = f"<span style='color: red;'>{location_details['message']}</span>"
        else:
            details = "\n".join(f"**{key}:** {value}" for key, value in location_details.items())
            self.displayInput.object = f"\n\n{details}"


    def switch_dropdown_options(self, event):
        """Switch dropdown options based on overview dropdown selection."""
        if event.new == '€ / ton CO₂':
            self.performance_dropdown.options = [
                'Choose performance',
                'Best CO₂ Capture: Cost €277-€453/ton',
                'Good CO₂ Capture: Cost €281-€496/ton',
                'Moderate CO₂ Capture: Cost €327-€501/ton',
                'Worst CO₂ Capture: Cost €357-€568/ton'
            ]
        elif event.new == 'kWh / ton':
            self.performance_dropdown.options = [
                'Choose performance',
                'Best Energy Efficiency: 500-700 kWh/ton',
                'Good Energy Efficiency: 700-900 kWh/ton',
                'Moderate Energy Efficiency: 900-1100 kWh/ton',
                'Worst Energy Efficiency: 1100-1300 kWh/ton'
            ]

    def update_slider(self, event):
        """Update slider range and label based on overview dropdown selection."""
        if event.new == '€ / ton CO₂':
            self.slider.name = 'Costs (€/ton)'
            self.slider.start = 270
            self.slider.end = 600
            self.slider.value = (270, 600)
            self.slider.format = '0.0a'
        elif event.new == 'kWh / ton':
            self.slider.name = 'Energy (kWh/ton)'
            self.slider.start = 500
            self.slider.end = 1300
            self.slider.value = (500, 1300)
            self.slider.format = '0[.]0'

    # Expose the layout for rendering
    def __panel__(self):
        return self._layout
