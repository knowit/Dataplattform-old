from .abstractTab import abstractTab
from .grid.Grid import Grid
from .Modules.fagtimerTimeSeriesModule import FagtimerTimeSeriesModule

class FagtimerTab(abstractTab):

    def __init__(self, app):
        self.grid = Grid(grid_id="fagtimer", num_rows=12, num_cols=12)
        self.grid.add_element(FagtimerTimeSeriesModule(app).get_module(), 0, 0, 12, 12)

    def get_tab(self):
        return self.grid.get_component()