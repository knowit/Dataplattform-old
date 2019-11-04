# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

class Grid:
	def __init__(self, width="100%", height="100%", grid_id="my_grid", num_rows=1, num_cols=1, grid_padding=5, padding=20):
		self.children = []
		self.grid_id = grid_id
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.grid_padding = grid_padding
		self.padding = padding

		grid_columns = ""
		grid_rows = ""
		for i in range(num_cols):
			grid_columns += str(1/num_cols * 100) + "% "
		for i in range(num_rows):
			grid_rows += str(1/num_rows * 100) + "% "
		self.style = {
				"padding": str(self.padding) + "px",
				"width": "calc(" + width + " - " + str(self.grid_padding * (self.num_cols - 1) + self.padding * 2) + "px)",
				"height": "calc(" + height +" - " + str(self.grid_padding * (self.num_rows - 1) + self.padding * 2) + "px)",
				"display": "grid",
				"gridTemplateColumns": grid_columns,
				"gridTemplateRows": grid_rows,
				"gridGap": grid_padding,
			}


	def add_element(self, element, col, row, width, height):
		if row > self.num_rows:
			raise ValueError(
				"Grid only has {:d} rows, not {:d}".format(
					self.num_rows, row
				)
			)
		if row + height> self.num_rows:
			raise ValueError(
				"Grid only has {:d} rows, not {:d} = {:d} + {:d}".format(
					self.num_rows, row + height, row, height
				)
			)
		if col > self.num_cols:
			raise ValueError(
				"Grid only has {:d} columns, not {:d}".format(
					self.num_cols, col
				)
			)
		if col + width> self.num_cols:
			raise ValueError(
				"Grid only has {:d} cols, not {:d} = {:d} + {:d}".format(
					self.num_cols, col + width, col, width
				)
			)

		self.children.append(html.Div(
			style={
				"width": "100%",
				"height": "100%",
				"gridRowStart": row + 1,
				"gridRowEnd": row + height + 1,
				"gridColumnStart": col + 1,
				"gridColumnEnd": col + width + 1,
			},
			children=element
		))


	def get_component(self):
		return html.Div(
			style=self.style,
			children=self.children,
			id=self.grid_id,
		)
