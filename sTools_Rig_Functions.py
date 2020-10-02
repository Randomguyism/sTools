from maya import cmds
from functools import partial

import sTools_Utilities as sUtil
reload(sUtil)

class RigFunctionsUI():
	def __init__(self, tabLayout, width, scrollBarThickness, buttonWidth, spacing):
		self.parentLayout = tabLayout
		self.tabWidth = width
		self.scrollWidth = scrollBarThickness
		self.buttonWidth = buttonWidth
		self.spacing = spacing

		self.rigTab()

	def rigTab(self):
		# Tab layout
		sUtil.tabLayout(name = 'Rig', parent = self.parentLayout, width = self.tabWidth, scrollBarThickness = self.scrollWidth)

		# FK/IK Match
		sUtil.toolTitle(label = 'FK/IK Joint Matching', ann = 'FK/IK Switch and Match Tool', spacing = self.spacing)
		cmds.text(label = 'WIP')
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.button(
			label = 'Placeholder', 
			ann = 'Placeholder button', 
			width = self.buttonWidth, 
			command = sUtil.test
			)
		cmds.separator(style = 'none', height = self.spacing[2])