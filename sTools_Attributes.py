from maya import cmds
from functools import partial

import sTools_Utilities as sUtil
reload(sUtil)

class AttributesUI():
	def __init__(self, tabLayout, width, scrollBarThickness, buttonWidth, spacing):
		self.parentLayout = tabLayout
		self.tabWidth = width
		self.scrollWidth = scrollBarThickness
		self.buttonWidth = buttonWidth
		self.spacing = spacing

		self.attributesTab()

	def attributesTab(self):
		# Tab layout
		sUtil.tabLayout(name = 'Attributes', parent = self.parentLayout, width = self.tabWidth, scrollBarThickness = self.scrollWidth)

		# Lock and Hide Attributes Tool
		sUtil.toolTitle(label = 'Lock and Hide', ann = 'Attribute visibility Tool', spacing = self.spacing)
		self.translateCheckBoxGrp = cmds.checkBoxGrp(
			label = 'Translate', 
			numberOfCheckBoxes = 4, 
			labelArray4 = ['X', 'Y', 'Z', 'All'], 
			columnWidth5 = [self.spacing[4], self.spacing[3], self.spacing[3], self.spacing[3], self.spacing[3]],
			)
		cmds.checkBoxGrp(
			self.translateCheckBoxGrp, 
			edit = True, 
			onCommand1 = partial(self.axisCheckBoxes, self.translateCheckBoxGrp),
			onCommand2 = partial(self.axisCheckBoxes, self.translateCheckBoxGrp),
			onCommand3 = partial(self.axisCheckBoxes, self.translateCheckBoxGrp),
			onCommand4 = partial(self.setAllCheckBoxes, self.translateCheckBoxGrp, True), 
			offCommand1 = partial(self.axisCheckBoxes, self.translateCheckBoxGrp),
			offCommand2 = partial(self.axisCheckBoxes, self.translateCheckBoxGrp),
			offCommand3 = partial(self.axisCheckBoxes, self.translateCheckBoxGrp),
			offCommand4 = partial(self.setAllCheckBoxes, self.translateCheckBoxGrp, False)
			)
		self.rotateCheckBoxGrp = cmds.checkBoxGrp(
			label = 'Rotate', 
			numberOfCheckBoxes = 4, 
			labelArray4 = ['X', 'Y', 'Z', 'All'], 
			columnWidth5 = [self.spacing[4], self.spacing[3], self.spacing[3], self.spacing[3], self.spacing[3]],
			onCommand4 = partial(sUtil.printButton, 'All rotate box checked'),
			offCommand4 = partial(sUtil.printButton, 'All rotate box unchecked')
			)
		cmds.checkBoxGrp(
			self.rotateCheckBoxGrp, 
			edit = True,
			onCommand1 = partial(self.axisCheckBoxes, self.rotateCheckBoxGrp),
			onCommand2 = partial(self.axisCheckBoxes, self.rotateCheckBoxGrp),
			onCommand3 = partial(self.axisCheckBoxes, self.rotateCheckBoxGrp),
			onCommand4 = partial(self.setAllCheckBoxes, self.rotateCheckBoxGrp, True), 
			offCommand1 = partial(self.axisCheckBoxes, self.rotateCheckBoxGrp),
			offCommand2 = partial(self.axisCheckBoxes, self.rotateCheckBoxGrp),
			offCommand3 = partial(self.axisCheckBoxes, self.rotateCheckBoxGrp),
			offCommand4 = partial(self.setAllCheckBoxes, self.rotateCheckBoxGrp, False)
			)
		self.scaleCheckBoxGrp = cmds.checkBoxGrp(
			label = 'Scale', 
			numberOfCheckBoxes = 4, 
			labelArray4 = ['X', 'Y', 'Z', 'All'], 
			columnWidth5 = [self.spacing[4], self.spacing[3], self.spacing[3], self.spacing[3], self.spacing[3]],
			onCommand4 = partial(sUtil.printButton, 'All scale box checked'),
			offCommand4 = partial(sUtil.printButton, 'All scale box unchecked')
			)
		cmds.checkBoxGrp(
			self.scaleCheckBoxGrp,
			edit = True,
			onCommand1 = partial(self.axisCheckBoxes, self.scaleCheckBoxGrp),
			onCommand2 = partial(self.axisCheckBoxes, self.scaleCheckBoxGrp),
			onCommand3 = partial(self.axisCheckBoxes, self.scaleCheckBoxGrp),
			onCommand4 = partial(self.setAllCheckBoxes, self.scaleCheckBoxGrp, True), 
			offCommand1 = partial(self.axisCheckBoxes, self.scaleCheckBoxGrp),
			offCommand2 = partial(self.axisCheckBoxes, self.scaleCheckBoxGrp),
			offCommand3 = partial(self.axisCheckBoxes, self.scaleCheckBoxGrp),
			offCommand4 = partial(self.setAllCheckBoxes, self.scaleCheckBoxGrp, False)
			)
		self.visibilityCheckBoxGrp = cmds.checkBoxGrp(
			label = 'Visibility',
			numberOfCheckBoxes = 1, 
			columnWidth2 = [self.spacing[4], self.spacing[3]] 
			)
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.text(label = 'Quick Selection')
		self.quickSelectionGrp = cmds.radioButtonGrp(
			label = '',
			labelArray4 = ['Fk', 'Ik', 'All', 'None'],
			numberOfRadioButtons = 4,
			columnWidth5 = [self.spacing[3] + 10, self.spacing[3], self.spacing[3], self.spacing[3], self.spacing[3]],
			onCommand1 = self.quickSelection,
			onCommand2 = self.quickSelection,
			onCommand3 = self.quickSelection,
			onCommand4 = self.quickSelection
			)
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.rowLayout(width = self.buttonWidth, numberOfColumns = 2)
		self.lockHideButton = cmds.button(
			label = 'Lock and Hide', 
			ann = 'Lock and hide selected attributes', 
			width = self.buttonWidth/2, 
			command = partial(self.getAttrSelection, True)
			)
		self.unlockShowButton = cmds.button(
			label = 'Unlock and Show', 
			ann = 'Unlock and show selected attributes', 
			width = self.buttonWidth/2, 
			command = partial(self.getAttrSelection, False)
			)
		cmds.setParent('..')
		cmds.separator(style = 'none', height = self.spacing[2])

		# Add Common Attributes Tool
		sUtil.toolTitle(label = 'Add Attributes', ann = 'Common Attributes Tool', spacing = self.spacing)
		cmds.text(label = 'WIP')
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.button(
			label = 'Placeholder', 
			ann = 'Placeholder button', 
			width = self.buttonWidth, 
			command = sUtil.test
			)
		cmds.separator(style = 'none', height = self.spacing[2])

	def axisCheckBoxes(self, checkBoxGrp, *args):
		checkBoxes = cmds.checkBoxGrp(checkBoxGrp, query = True, valueArray4 = True)

		if checkBoxes[0] and checkBoxes[1] and checkBoxes[2]:
			# If all axis boxes are checked check 'All'
			cmds.checkBoxGrp(checkBoxGrp, edit = True, value4 = True)

		elif not checkBoxes[3]:
			# If 'All' is unchecked and an axis box is unchecked do nothing
			return

		elif not checkBoxes[0] or not checkBoxes[1] or not checkBoxes[2]:
			# if 'All' is checked and an axis box is unchecked then uncheck 'All'
			cmds.checkBoxGrp(checkBoxGrp, edit = True, value4 = False)

	def setAllCheckBoxes(self, checkBoxGrp, state, *args):
		# Sets all check boxes in group to state value
		if state:
			cmds.checkBoxGrp(checkBoxGrp, edit = True, valueArray4 = [True, True, True, True])

		elif not state:
			cmds.checkBoxGrp(checkBoxGrp, edit = True, valueArray4 = [False, False, False, False])

	def quickSelection(self, *args):
		selected = cmds.radioButtonGrp(self.quickSelectionGrp, query = True, select = True)
		
		# Set appropriate bools for lock/hide based on selected radioButton 
		if selected == 1:
			self.setAllCheckBoxes(self.translateCheckBoxGrp, True)
			self.setAllCheckBoxes(self.rotateCheckBoxGrp, False)
			self.setAllCheckBoxes(self.scaleCheckBoxGrp, True)

		elif selected == 2:
			self.setAllCheckBoxes(self.translateCheckBoxGrp, False)
			self.setAllCheckBoxes(self.rotateCheckBoxGrp, True)
			self.setAllCheckBoxes(self.scaleCheckBoxGrp, True)

		elif selected == 3:
			self.setAllCheckBoxes(self.translateCheckBoxGrp, True)
			self.setAllCheckBoxes(self.rotateCheckBoxGrp, True)
			self.setAllCheckBoxes(self.scaleCheckBoxGrp, True)
			cmds.checkBoxGrp(self.visibilityCheckBoxGrp, edit = True, value1 = True)

		elif selected == 4:
			self.setAllCheckBoxes(self.translateCheckBoxGrp, False)
			self.setAllCheckBoxes(self.rotateCheckBoxGrp, False)
			self.setAllCheckBoxes(self.scaleCheckBoxGrp, False)
			cmds.checkBoxGrp(self.visibilityCheckBoxGrp, edit = True, value1 = False)

	def lockHideAttr(self, obj, attribute, checkBoxState, lock):
		if not checkBoxState:
			# If the check box is unchecked do nothing for that attribute
			return

		elif lock:
			cmds.setAttr(obj + attribute, keyable = False, lock = True)

		elif not lock:
			cmds.setAttr(obj + attribute, keyable = True, lock = False)

	def getAttrSelection(self, lock, *args):
		sel = cmds.ls(selection = True)
		attributeList = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.v']

		# Get lists of bools for lock/hide attribute checkBoxes
		translate = cmds.checkBoxGrp(self.translateCheckBoxGrp, query = True, valueArray4 = True)
		rotate = cmds.checkBoxGrp(self.rotateCheckBoxGrp, query = True, valueArray4 = True)
		scale = cmds.checkBoxGrp(self.scaleCheckBoxGrp, query = True, valueArray4 = True)
		visibility = cmds.checkBoxGrp(self.visibilityCheckBoxGrp, query = True, value1 = True)

		# Remove 'all' checkBox state from arrays
		translate.pop()
		rotate.pop()
		scale.pop()

		# Combine the lists into one checkBoxList
		checkBoxList = []
		checkBoxList.extend(translate)
		checkBoxList.extend(rotate)
		checkBoxList.extend(scale)
		checkBoxList.append(visibility)

		for each in sel:
			# For each attribute lock/unlock based on selected checkBoxes
			for attribute, checkBoxState in zip(attributeList, checkBoxList):
				self.lockHideAttr(each, attribute, checkBoxState, lock)