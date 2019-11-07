from .abstractTab import abstractTab
from .grid.Grid import Grid
from .Modules.twitterSearchHashtagModule import TwitterSearchHashtagModule
from .Modules.twitterSearchTimeSeriesModule import TwitterSearchTimeSeriesModule
from .Modules.twitterAccountTimeSeriesModule import TwitterAccountTimeSeriesModule


class TwitterTab(abstractTab):

    def __init__(self, app):
        self.grid = Grid(grid_id="twitter", num_rows=12, num_cols=12)
        self.grid.add_element(TwitterSearchHashtagModule().get_module(), 6, 0, 3, 6)
        self.grid.add_element(TwitterSearchTimeSeriesModule().get_module(), 0, 0, 6, 6)
        self.grid.add_element(TwitterAccountTimeSeriesModule().get_module(), 0, 6, 6, 6)

    def get_tab(self):
        return self.grid.get_component()