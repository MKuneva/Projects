import panel as pn

class NavTabs(pn.viewable.Viewer):
    def __init__(self, overview_content):
        super().__init__()

        # Create a Tabs layout, passing the Overview content as one of the tabs
        self._layout = pn.Tabs(
            ("Location Sensitivity", overview_content),  # Correct way to pass a tab label and content
            tabs_location="left",
            styles={
                'font-size': '12px',                 
                'font-weight': 'bold', 
                'height':'85vh',        
            }
        )

    # Expose the layout for rendering
    def __panel__(self):
        return self._layout