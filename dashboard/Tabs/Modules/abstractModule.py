# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
from abc import ABC, abstractmethod

class abstractModule(ABC):

	style={"width": "100%", "height": "100%"}

	@property 
	def graph_style(self):
		return self.style


	@abstractmethod
	def get_module(self):
		raise NotImplementedError





