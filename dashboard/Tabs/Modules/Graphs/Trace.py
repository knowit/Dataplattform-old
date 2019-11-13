import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from typing import Union

class Trace():

	def __init__(self, data, data_layout = [], trace_mode="lines",
			trace_type="scatter", colors = ["#0c956e", "#003299", "red"],
			title="", names=[], shape=["linear"], smoothing=[0.8], 
			axis_text=["X-axis", "Y-axis"], axis_type=["linear", "linear"],
			plot_bgcolor="#ffffff", grid_color="rgba(0, 0, 0, 0.1)", 
			paper_bgcolor="#fffaf3", show_legend=True, line_dash=["solid"],
			line_fill=Union[dict, str]):

		if data_layout == []:
			for i in range(0, len(data.columns), 2):
				print(i)
				data_layout.append([data.columns[i], data.columns[i+1 if i+1 < len(data.columns) else i]])


		self.traces = []
		for i in range(len(data_layout)):
			#cur_data = data[[data_layout[i][0], data_layout[i][1]]].copy().dropna()
			trace = {
					"mode": trace_mode,
					"type": trace_type,
					"name": names[i] if i < len(names) else "Trace",
					"x": data[data_layout[i][0]],
					"y": data[data_layout[i][1]],
					"line": {
						"dash": line_dash[i] if i < len(line_dash) else line_dash[0],
						"color": colors[i] if i < len(colors) else "blue",
						"shape": shape[i] if i < len(shape) else shape[0],
						"smoothing": smoothing[i] if i < len(smoothing) else smoothing[0],
					},
				}

			if isinstance(line_fill, (list, str)):
				if isinstance(line_fill, list):
					if i == line_fill[1]:
						trace["fill"] = line_fill[0]
						self.traces.insert(0, trace)
					else:
						self.traces.append(trace)
				else:
					trace["fill"] = line_fill
					self.traces.append(trace)

			else:
				self.traces.append(trace)

		layout = {
			"title": {
				"text": title,
				},
			"xaxis": {
				"type": axis_type[0],
				"title": {
					"text": axis_text[0],
				},
				"autorange": True,
				"gridcolor": grid_color,
			},
			"yaxis": {
				"type": axis_type[1] if 1 < len(axis_type) else "linear",
				"title": {
					"text": axis_text[1] if 1 < len(axis_text) else "Y-axis",
				},
				"autorange": True,
				"gridcolor": grid_color,
			},
			"plot_bgcolor": plot_bgcolor,
			"paper_bgcolor": paper_bgcolor,
			"showlegend": show_legend,
		}
		self.fig = go.Figure(data=self.traces, layout=layout)



	def get_trace(self):
		return self.fig


class Bar():

	def __init__(self, data, data_layout=[], trace_type="bar",
				 colors=["#0c956e", "blue", "red"], title="",
				 names=[], axis_text=["X-axis", "Y-axis"],
				 axis_type=["linear", "linear"], plot_bgcolor="#ffffff",
				 grid_color="rgba(0, 0, 0, 0.1)", paper_bgcolor="#fffaf3",
				 orientation="v", show_legend=True, show_xaxis_text=True,
				 show_yaxis_text=True, barmode="group"):


		if data_layout == []:
			for i in range(0, len(data.columns), 2):
				print(i)
				data_layout.append([data.columns[i], data.columns[i+1 if i+1 < len(data.columns) else i]])

		self.traces = []
		for i in range(len(data_layout)):
			# cur_data = data[[data_layout[i][0], data_layout[i][1]]].copy().dropna()
			trace = {
				"type": trace_type,
				"name": names[i] if i < len(names) else "Trace",
				"orientation": orientation,
				"x": data[data_layout[i][0]],
				"y": data[data_layout[i][1]],
				"marker": {"color": colors[i]}

			}

			self.traces.append(trace)

		layout = {
			"title": {
				"text": title,
			},
			"xaxis": {
				"autorange": True,
				"gridcolor": grid_color,
			},
			"yaxis": {
				"autorange": True,
				"gridcolor": grid_color,
			},
			"plot_bgcolor": plot_bgcolor,
			"paper_bgcolor": paper_bgcolor,
			"showlegend": show_legend,
			"barmode": barmode,
		}


		self.fig = go.Figure(data=self.traces, layout=layout)

		if show_xaxis_text:
			self.fig.update_layout(
				xaxis_title=axis_text[0],
			)
		if show_yaxis_text:
			self.fig.update_layout(
				yaxis_title=axis_text[1] if 1 < len(axis_text) else "Y-axis",
			)

	def get_trace(self):
		return self.fig


class Pie():

	def __init__(self, values, labels,
				 colors=["#0c956e", "blue", "red"],
				 title="", plot_bgcolor="#ffffff",
				 grid_color="rgba(0, 0, 0, 0.1)", paper_bgcolor="#fffaf3"):

		fig_data = [
			{
				'labels': labels,
				'values': values,
				'type': 'pie',
				'marker': {'colors': colors}
			}
		]

		layout = {
			"margin": go.layout.Margin(
        l=20,
        r=20,
        b=20,
        t=20
    ),
			"title": {
				"text": title,

			},
			"plot_bgcolor": plot_bgcolor,
			"paper_bgcolor": paper_bgcolor,
		}

		self.fig = go.Figure(data=fig_data, layout=layout)


	def get_trace(self):
		return self.fig
