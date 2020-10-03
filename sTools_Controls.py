from maya import cmds
from functools import partial

import sTools_Utilities as sUtil
reload(sUtil)

class ControlsUI():
	def __init__(self, tabLayout, width, scrollBarThickness, buttonWidth, spacing):
		self.parentLayout = tabLayout
		self.tabWidth = width
		self.scrollWidth = scrollBarThickness
		self.buttonWidth = buttonWidth
		self.spacing = spacing

		self.controlsTab()

	def controlsTab(self):
		# Tab layout
		sUtil.tabLayout(name = 'Controls', parent = self.parentLayout, width = self.tabWidth, scrollBarThickness = self.scrollWidth)

		# Create Circular Controls		
		sUtil.toolTitle(label = 'Create Controls', ann = 'Control Creation Tool', spacing = self.spacing)
		cmds.text(label = 'Select all joints to add controls to.')
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.text(label = "Joints should have a '_jnt' suffix", font = 'obliqueLabelFont')
		cmds.separator(style = 'none', height = self.spacing[0])
		self.constraintType = cmds.radioButtonGrp(
			label = 'Constraint Type',
			ann = 'Selection for type of constraint between joints and controls',
			labelArray3 = ['Parent', 'Point', 'Orient'],
			numberOfRadioButtons = 3,
			columnWidth4 = [self.spacing[4], self.spacing[3], self.spacing[3], self.spacing[3]]
			)
		self.controlAxis = cmds.radioButtonGrp(
			label = 'Control Axis',
			ann = 'Selection for the axis corresponding with the desired normal of created controls',
			labelArray3 = ['X', 'Y', 'Z'],
			numberOfRadioButtons = 3,
			columnWidth4 = [self.spacing[4], self.spacing[3], self.spacing[3], self.spacing[3]]
			)
		self.controlRadius = cmds.intSliderGrp(
			field = True, 
			label = 'Control Radius', 
			ann = "Radius for created circular controls", 
			minValue = 5, 
			maxValue = 25,
			value = 5,
			step = 5
			)
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.button(
			label = 'Create', 
			ann = 'Creates circular controls and joint constraints', 
			width = self.buttonWidth, 
			command = partial(self.createControlsButton, self.constraintType, self.controlAxis, self.controlRadius)
			)
		cmds.separator(style = 'none', height = self.spacing[2])

	def createControlsButton(self, conType, axis, radius, *args):
		constraintType = cmds.radioButtonGrp(conType, query = True, select = True)
		controlAxis = cmds.radioButtonGrp(axis, query = True, select = True)
		ctrlAxis = [0, (1, 0, 0), (0, 1, 0), (0, 0, 1)]
		ctrlRadius = cmds.intSliderGrp(radius, query = True, value = True)

		self.createControls(constraintType, ctrlAxis[controlAxis], ctrlRadius)

	def createControls(self, constraintType, ctrlAxis, ctrlRadius):
		sel = cmds.ls(selection = True)

		for x in sel:
			ctrlName = x.replace("_jnt", "_ctrl")
			ctrl = cmds.circle(normal = ctrlAxis, radius = ctrlRadius, name = ctrlName)[0]
			group = cmds.group(ctrl, name = ctrl + "_auto")
			offset = cmds.group(group, name = ctrl + "_offset")
			cmds.parentConstraint(x, offset, maintainOffset = False)
			cmds.delete(cmds.parentConstraint(x, offset))
			if constraintType == 1:
				cmds.parentConstraint(ctrl, x, maintainOffset = False)
			elif constraintType == 2:
				cmds.pointConstraint(ctrl, x, maintainOffset = False)
			elif constraintType == 3:
				cmds. orientConstraint(ctrl, x, maintainOffset = False)
			print('Created control for ' + x)
