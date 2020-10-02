from maya import cmds as cmds

def tabLayout(name, parent, width, scrollBarThickness):
		tab = cmds.scrollLayout(parent = parent, verticalScrollBarThickness = scrollBarThickness, verticalScrollBarAlwaysVisible = True)
		cmds.columnLayout(adjustableColumn = True,  width = width)
		cmds.tabLayout(parent, edit = True, tabLabel = (tab, name))

def toolTitle(label, ann, spacing):
		cmds.separator(style = 'in', horizontal = True, height = spacing[0])
		cmds.text(label = label, ann = ann, font = 'boldLabelFont', height = spacing[1])
		cmds.separator(style = 'out', horizontal = True, height = spacing[0])

def test(*args):										# Test function
	print('This funciton was called correctly.')

def printButton(data, *args):							# Test function
	print(data)

def printData(data):									# Test function
	print(data)