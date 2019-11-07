from .abstractTab import abstractTab
from .grid.Grid import Grid
from .Modules.slackTimeSeriesModule import SlackModule, Slack3DGraph


class SlackTab(abstractTab):

	def __init__(self, app):
		self.grid = Grid(grid_id="slack", num_rows=12, num_cols=12)
		self.grid.add_element(SlackModule().get_module(), 0, 0, 12, 12)
		#self.grid.add_element(Slack3DGraph().get_module(), 6, 0, 6, 6)


	def get_tab(self):
		return self.grid.get_component()
