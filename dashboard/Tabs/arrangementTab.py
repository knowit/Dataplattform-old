from .abstractTab import abstractTab
from .grid.Grid import Grid
from .Modules.arrangementTimeSeriesModule import ArrangementTimeSeriesModule
from .Modules.arrangementResponseBarModule import ArrangementResponseBarModule
from .Modules.arrangementResponsePieModule import ArrangementResponsePieModule

class ArrangementTab(abstractTab):

    def __init__(self, app):
        self.grid = Grid(grid_id="arrangement", num_rows=12, num_cols=12)
        self.grid.add_element(ArrangementTimeSeriesModule(app).get_module(), 0, 0, 6, 6)
        self.grid.add_element(ArrangementResponseBarModule(app).get_module(), 0, 6, 6, 6)
        self.grid.add_element(ArrangementResponsePieModule(app).get_module(), 6, 0, 3, 6)



    def get_tab(self):
        return self.grid.get_component()

