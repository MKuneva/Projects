import panel as pn
from overview import Overview  
from nav_tabs import NavTabs  


pn.extension(
    sizing_mode="stretch_width",
    css_files=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
    ],
)

class App(pn.viewable.Viewer):

    def __init__(self):
        super().__init__()
        # Create an instance of the Overview class
        overview = Overview()
        # Create an instance of the NavTabs class, passing the Overview content to it
        self._tabs = NavTabs(overview)
        # Create the BootstrapTemplate
        self._layout = pn.template.BootstrapTemplate(
            title="Carbyon",
            header_background="#41abff",
            main=pn.Row(self._tabs)
            )
         
    # Expose the layout for rendering
    def __panel__(self):
        return self._layout
    
# Serve the app
app = App()
app.servable()
