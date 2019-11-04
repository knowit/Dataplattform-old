from .grid.Grid import Grid
from abc import ABC, abstractmethod


class abstractTab(ABC):

	style={"width": "100%", "height": "100%"}

	@property
	def tab_style(self):
		return self.tab_style
	

	@abstractmethod
	def get_tab(self):
		raise NotImplementedError
