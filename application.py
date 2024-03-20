from PySide6.QtWidgets import QApplication

class Application (QApplication):

	_instance = None

	def __init__(self, args):
		super(Application, self).__init__(args)

		Application.setInstance(self)

	def setInstance(inst):
		Application._instance = inst

	def getInstance():
		return Application._instance