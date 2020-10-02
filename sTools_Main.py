from maya import cmds as cmds
from functools import partial

import random

import sTools_Rename as sRename
import sTools_Joint_Functions as sJoint
import sTools_Controls as sControl
import sTools_Attributes as sAttributes
import sTools_Rig_Functions as sRig

reload(sRename)
reload(sJoint)
reload(sControl)
reload(sAttributes)
reload(sRig)

class UI(object):
	def __init__(self):
		self.winName = 'sTools'							# Window variables
		self.winTitle = 'sTools Window'
		self.defaultFontSize = 14						# Set this to scale window to the font size of maya
		self.winWidth = self.defaultFontSize * 30
		self.winHeight = self.defaultFontSize * 65
	
		if cmds.window(self.winName, exists = True):	# Delete window if it already exists
			cmds.deleteUI(self.winName)

		self.buildUI()									# Build the window

	def buildUI(self, *args):
		self.mainWin = cmds.window(self.winName, width = self.winWidth, height = self.winHeight, title = self.winTitle, sizeable = False)
		
		# Main Layout
		mainCL = cmds.columnLayout(adjustableColumn = True)

		# Layout variables
		mainWidths = [self.winWidth * 0.8, self.winWidth * 0.2]
		mainHeights = [self.winHeight * 0.89, self.winHeight * 0.09, self.winHeight * 0.02]
		scrollWidth = self.defaultFontSize + 6
		tabWidth = self.winWidth - scrollWidth
		buttonWidth = self.defaultFontSize * 28
		spacing = [
			self.defaultFontSize * 0.8, 
			self.defaultFontSize * 1.5, 
			self.defaultFontSize * 3.5, 
			self.defaultFontSize * 4.5,
			self.defaultFontSize * 10
			]

		# Header Layout
		headerRL = cmds.rowLayout(
			width = self.winWidth, 
			height = mainHeights[1], 
			numberOfColumns = 2, 
			columnWidth2 = mainWidths, 
			rowAttach = (2, 'top', 0)
			)
		cmds.columnLayout(width = mainWidths[0], adjustableColumn = True)
		cmds.text(label = 'Rigging Tools', font = 'obliqueLabelFont')
		cmds.columnLayout(parent = headerRL, width = mainWidths[1])
		cmds.button(
			label = 'Error', 
			ann = 'This helpful button creates random errors', 
			width = mainWidths[1], 
			height = mainHeights[1], 
			command = self.errorButton
			)

		# Main Body Tab Layout
		cmds.formLayout(parent = mainCL, height = mainHeights[0])
		pane = cmds.paneLayout(configuration = 'horizontal2', width = self.winWidth, height = mainHeights[0], paneSize = [1, 100, 80])
		self.tabs = cmds.tabLayout(innerMarginWidth = 5, innerMarginHeight = 5)

		tab_kwargs = {
			'tabLayout' : self.tabs, 
			'width' : tabWidth, 
			'scrollBarThickness' : scrollWidth, 
			'buttonWidth' : buttonWidth, 
			'spacing' : spacing
			}

		# Tab 1 - Renaming Tools
		sRename.RenameUI(**tab_kwargs)

		# Tab 2 - Joint Tools
		sJoint.JointsUI(**tab_kwargs)

		# Tab 3 - Control Tools
		sControl.ControlsUI(**tab_kwargs)

		# Tab 4 - Attribute Tools
		sAttributes.AttributesUI(**tab_kwargs)

		# Tab 5 - Rig Tools
		sRig.RigFunctionsUI(**tab_kwargs)

		# Notes Section
		self.notes = cmds.columnLayout(parent = pane)
		cmds.text(label = 'Notes')
		self.notesField = cmds.scrollField(editable = True, wordWrap = True, width = self.winWidth, height = 11 * self.defaultFontSize, 
			text = '''To do: Add attributes, Lock and hide, FKIK joint mirroring, Control shape library.''')
		cmds.scrollField(self.notesField, edit = True, changeCommand = partial(self.setNotesHeight, self.notesField))
				
		# Helpline Footer
		self.form2 = cmds.formLayout(parent = mainCL, width = self.winWidth, height = mainHeights[2])
		self.lineHelp = cmds.helpLine()
		cmds.formLayout(self.form2, edit = True, attachForm = ( (self.lineHelp, 'left', 0), (self.lineHelp, 'bottom', 0), (self.lineHelp, 'right', 0) ))

		# Show and Resize Window
		cmds.showWindow(self.winName)
		cmds.window(self.winName, edit = True, width = self.winWidth, height = self.winHeight)

	def setNotesHeight(self, field, *args):										# This function checks the height of the notes field
		lineNumber = cmds.scrollField(field, query = True, numberOfLines = True)
		currentHeight = cmds.scrollField(field, query = True, height = True)
	
		if lineNumber < 10:														# Sets height to minimum if not enough lines
			cmds.scrollField(field, edit = True, height = 11 * self.defaultFontSize)
		elif lineNumber >= 25:													# Sets height to maximum if too many lines
			cmds.scrollField(field, edit = True, height = 26 * self.defaultFontSize)
		else:																	# Sets height to just the right height for number of lines
			newHeight = (lineNumber + 1) * self.defaultFontSize
			cmds.scrollField(field, edit = True, height = newHeight)

	def errorButton(*args):
		errorList = [
			"><>",
			"cuttlefish",
			"Something probably just broke!",
			"Invalid syntax",
			"Global name 'cuttlefish' is not defined",
			"Object '><>' not found.",
			"Invalid flag 'cuttlefish'",
			"cannot concatenate 'cuttlefish' and '><>' objects",
			"'><>' object has no attribute 'cuttlefish'"
			]
		randomError = random.choice(errorList)				# Chooses a random string from list to input in error command
		cmds.error(randomError)								# pointless but fun