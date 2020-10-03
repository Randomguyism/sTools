from maya import cmds
from functools import partial

import sTools_Utilities as sUtil
reload(sUtil)

class JointsUI():
	def __init__(self, tabLayout, width, scrollBarThickness, buttonWidth, spacing):
		self.parentLayout = tabLayout
		self.tabWidth = width
		self.scrollWidth = scrollBarThickness
		self.buttonWidth = buttonWidth
		self.spacing = spacing

		self.jointTab()

	def jointTab(self):
		# Tab layout
		sUtil.tabLayout(name = 'Joints', parent = self.parentLayout, width = self.tabWidth, scrollBarThickness = self.scrollWidth)

		# Joint Splitter
		sUtil.toolTitle(label = 'Joint Splitter', ann = 'Joint Splitter Tool', spacing = self.spacing)
		cmds.text(label = 'First select the parent joint and then the child joint.')
		cmds.separator(style = 'none', height = self.spacing[0])
		self.jointNum = cmds.intSliderGrp(
			field = True, 
			label = 'Number of Joints', 
			ann = 'Number of joints to insert', 
			minValue = 1, 
			maxValue = 10, 
			fieldMaxValue = 20
			)
		self.jointAxis = cmds.radioButtonGrp(
			label = 'Translation Axis', 
			ann = 'Selection for which axis joints are translated in', 
			labelArray3 = ['X', 'Y', 'Z'], 
			numberOfRadioButtons = 3, 
			columnWidth4 = [self.spacing[4], self.spacing[3], self.spacing[3], self.spacing[3]]
			)
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.button(
			label = 'Split', 
			ann = 'Inserts a number of joints between the two selected joints', 
			width = self.buttonWidth, 
			command = partial(self.jointSpliterButton, self.jointNum, self.jointAxis))
		cmds.separator(style = 'none', height = self.spacing[2])

	def jointSpliterButton(self, jointNumber, xyz, *args):
		# Finds the requested number of joints to insert
		jointNum = cmds.intSliderGrp(jointNumber, query = True, value = True)
		# Indicates which axis joints are translated in
		jointAxis = cmds.radioButtonGrp(xyz, query = True, select = True)
		attr = ['.tx', '.ty', '.tz']

		if jointAxis == 0:
			# Errors if no axis is selected
			cmds.error('Joint translation axis not selected')
			
		# Checks which axis is selected and sends data to function
		elif jointAxis == 1:
			self.jointSplit(jointNum, jointAxis, attr[0])
		elif jointAxis == 2:
			self.jointSplit(jointNum, jointAxis, attr[1])
		elif jointAxis == 3:
			self.jointSplit(jointNum, jointAxis, attr[2])

	def jointSplit(self, jointNum, jointAxis, attr):
		sel = cmds.ls(selection = True, dag = True)
		parent = sel[0]
		child = sel[1]
	
		jointLength = cmds.getAttr(child + attr)
		translation = jointLength / (jointNum + 1)
		if jointAxis == 1:
			x = translation
			y = z = 0
		elif jointAxis == 2:
			y = translation
			x = z = 0
		elif jointAxis == 3:
			z = translation
			x = y = 0

		for i in range (1, jointNum + 1):
			newJoint = cmds.insertJoint(parent)
			newJoint = cmds.rename(newJoint, 'split' + str(i))
			cmds.move(x, y, z, newJoint+'.scalePivot', newJoint+'.rotatePivot', relative = True, objectSpace = True)
			parent = newJoint
			cmds.select(newJoint)

		print('Split ' + parent + ' into ' + str(jointNum + 1) + ' joints')
