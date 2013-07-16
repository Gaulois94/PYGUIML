import sfml as sf
from EventManager import EventManager

class Updatable:
	"""Basic class who can update a child hierarchy"""
	_focusIsChecked = False
	def __init__(self, parent=0):
		self._changeWindow = False
		self._event = None
		self._child = list()
		self._parent = None
		self.canUpdate = True
		self.setParent(parent)

	def __del__(self):
		self.parent = 0
		for it in self._child:
			self.removeChild(it)

	def updateFocus(self):
		for child in self._child[::-1]:
			if self._focusIsChecked:
				return
			if child._child != []:
				Updatable.updateFocus(child)
			else:
				child.updateFocus()

	def update(self, render=None):
		"""THIS methode Update all child of this Widget. 
		It launch them Update() for drawing there"""

		for child in self._child:
			child.update(render)
		self._changeWindow=False
	
	def removeChild(self, child):
		"""Remove child in the object"""
		try:
			if isinstance(child, Updatable):
				self._child.remove(child)
			else:
				del self._child[child]
		except ValueError:
			print("child is not a child of self._child")
			return False
		except IndexError:
			print("can't find the child index in self._child")
			return False
		else:
			return True

		child._parent = 0

	def addChild(self, child, pos="End"):
		"""child become a widget's child"""
		if child._parent is not self:
			child._parent = self,pos
	
		if pos=="End":
			pos = len(self._child)
		if not self.isChild(child):
			self._child.insert(pos, child)

	def isChild(self, child):
		""" This methode say if child is a widget's child"""
		return child in self._child
	
	def getEventFromRootParent(self):
		if isinstance(self._parent, Updatable):
			return self._parent.getEventFromRootParent()
		return None

	def getRender(self):
		if isinstance(self._parent, Updatable):
			return self._parent.getRender()
		else:
			return None

	def setParent(self, parent, pos="End"):
		"""Set the Updatable's parent"""

		if isinstance(self._parent, Updatable):
			self._parent.removeChild(self)

		event = self.getEventFromRootParent()
		self._parent = parent
		self._event = self.getEventFromRootParent()

		if event is not self._event:
			self._changeWindow = True

		if isinstance(self._parent, Updatable):
			self._parent.addChild(self, pos)

	def _getParentList(self):
		parentList = []
		if self._parent:
			parentList.append(self._parent)
			parentList.extend(self._parent._getParentList())
		return parentList

	parent = property(lambda self:self._parent,\
			lambda self, parent: self.setParent(parent))
	child = property(lambda self:self._child)
	changeWindow = property(lambda self:self._changeWindow)
	event = property(lambda self:self._event)
	parentList = property(lambda self:self._getParentList())