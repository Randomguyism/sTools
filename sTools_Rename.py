from maya import cmds
from functools import partial

import sTools_Utilities as sUtil
reload(sUtil)

class RenameUI():
	def __init__(self, tabLayout, width, scrollBarThickness, buttonWidth, spacing):
		self.parentLayout = tabLayout
		self.tabWidth = width
		self.scrollWidth = scrollBarThickness
		self.buttonWidth = buttonWidth
		self.spacing = spacing

		self.renameTab()

	def renameTab(self):
		# Tab layout
		sUtil.tabLayout(name = 'Rename', parent = self.parentLayout, width = self.tabWidth, scrollBarThickness = self.scrollWidth)

		# Prefix Tool
		sUtil.toolTitle(label = 'Add Prefix', ann = 'Prefix Tool', spacing = self.spacing)
		self.prefixText = cmds.textFieldGrp(label = 'Prefix')
		self.prefixScore = cmds.checkBoxGrp(label = 'Underscore', ann = "Adds an '_' after the prefix in the new name", value1 = True)
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.button(
			label = 'Add', 
			ann = 'Adds prefix to selected objects', 
			width = self.buttonWidth, 
			command = partial(self.addPrefixSuffixButton, self.prefixText, 'Prefix', self.prefixScore)
			)
		cmds.separator(style = 'none', height = self.spacing[2])

		# Suffix Tool
		sUtil.toolTitle(label = 'Add Suffix', ann = 'Suffix Tool', spacing = self.spacing)
		self.suffixText = cmds.textFieldGrp(label = 'Suffix')
		self.suffixScore = cmds.checkBoxGrp(label = 'Underscore', ann = "Adds an '_' before the suffix in the new name", value1 = True)
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.button(
			label = 'Add', 
			ann = 'Adds suffix to selected objects', 
			width = self.buttonWidth, 
			command = partial(self.addPrefixSuffixButton, self.suffixText, 'Suffix', self.suffixScore)
			)
		cmds.separator(style = 'none', height = self.spacing[2])

		# Rename Tool
		sUtil.toolTitle(label = 'Rename', ann = 'Rename Tool', spacing = self.spacing)
		self.renameText = cmds.textFieldGrp(label = 'Rename')
		self.renamePadding = cmds.intSliderGrp(
			field = True, 
			label = 'Padding', 
			ann = "Amount of digits displayed in the numbers of the new name", 
			minValue = 1, 
			maxValue = 5,
			value = 1
			)
		self.renameStart =  cmds.intFieldGrp(label = 'Start Number', ann = 'Start number for object count when renaming multiple objects', value1 = 1)
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.button(
			label = 'Rename', 
			ann = 'Renames and numbers selected objects', 
			width = self.buttonWidth, 
			command = partial(self.renameButton, self.renameText, self.renamePadding, self.renameStart)
			)
		cmds.separator(style = 'none', height = self.spacing[2])

		# Search and Replace Tool
		sUtil.toolTitle(label = 'Search and Replace', ann = 'Replace Names Tool', spacing = self.spacing)
		cmds.text(label = 'WIP')
		cmds.separator(style = 'none', height = self.spacing[0])
		cmds.button(
			label = 'Placeholder', 
			ann = 'Placeholder button', 
			width = self.buttonWidth, 
			command = sUtil.test
			)
		cmds.separator(style = 'none', height = self.spacing[2])

	def addPrefixSuffixButton(self, textField, fieldType, checkBox, *args):			# Queries text entered into UI and underscore checkbox state
		data = cmds.textFieldGrp(textField, query = True, text = True)
		checkBox = cmds.checkBoxGrp(checkBox, query = True, value1 = True)

		if data == "":
			cmds.error(fieldType + " field is empty")
		else:
			if fieldType == 'Prefix':												# Checks if prefix is being added and sends data to function
				self.addPrefix(data, checkBox)
			elif fieldType == 'Suffix':												# Checks if suffix is being added and sends data to function
				self.addSuffix(data, checkBox)

	def renameButton(self, textField, padding, startNumber, *args):
		newName = cmds.textFieldGrp(textField, query = True, text = True)			# Finds the new name from UI text field
		pad = cmds.intSliderGrp(padding, query = True, value = True)				# Ammount of zero padding for zfill
		start = cmds.intFieldGrp(startNumber, query = True, value1 = True)			# Start number for renaming multiple objects

		if newName == "":
			cmds.error("Rename field is empty")
		else:
			self.rename(newName, pad, start)										# Sends data to rename function

	def addPrefix(self, prefix, checkBox):
		sel = cmds.ls(selection = True, dag = True)
	
		if not sel:																	# Error exeption if nothing selected
			cmds.error("There is nothing in selection")

		else:
			if checkBox:															# Adds underscore after prefix if UI box is checked
				u = prefix + '_'
			else:
				u = prefix

			for x in sel:															# Renames objects with prefix plus original name
				newName = u + str(x)
				cmds.rename(x, newName)
				print('renamed ' + x + ' to ' + newName)

	def addSuffix(self, suffix, checkBox):
		sel = cmds.ls(selection = True, dag = True)

		if not sel:																	# Error exeption if nothing selected
			cmds.error("There is nothing in selection")

		else:
			if checkBox:															# Adds underscore before suffix if UI box is checked
				u = '_' + suffix
			else:
				u = suffix

			for x in sel:															# Renames objects with original name plus suffix
				newName = str(x) + u
				cmds.rename(x, newName)
				print('renamed ' + x + ' to ' + newName)

	def rename(self, name, padding, startNumber):									# Will sometimes break because og short names need to implement \n
		sel = cmds.ls(selection = True, dag = True)									# a method using long names

		for i, x in enumerate(sel):
			n = startNumber + i
			num = str(n)
			newName = name + num.zfill(padding)
			cmds.rename(x, newName)
			print('renamed ' + x + ' to ' + newName)

	# def replaceTest(self, search, replace, *args):
	# 	sel = cmds.ls(selection = True, dag = True, long = True)

	# 	for x in sel:
	# 		shortName = x.split('|')[-1]
	# 		children = cmds.listRelatives(x, children = True, fullPath = True) or []
	# 		if len(children) == 1:
	# 			child = children[0]
	# 			objtype = cmds.objectType(child)

	# 		else:
	# 			objtype = cmds.objectType(x)

	# 		newName = shortName + '_' + suffix
	# 		cmds.rename(search, x.replace(search, replace))
	# 		print(sel)
	# 		print(x)
	# 		print(search)
	# 		print(replace)