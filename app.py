from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QCommandLineParser, QCoreApplication
from PySide6.QtGui import QIcon
import sys, os
from menus import Menu
from media import Media
from application import Application

print(Application.getInstance())
app 	= Application(sys.argv)

app.setStyle("Fusion")


class Player (QMainWindow):

	instance = None

	def __init__(self):
		super(Player, self).__init__()
		self.resize(800, 600)
		self.init()

	def init(self):
		Menu.config(self)
		self.parser = QCommandLineParser()
		self.parser.addPositionalArgument("file", 
			QCoreApplication.translate("main", "The file to open.")
		)
		self.parser.process(app)

		# Get files
		self.files = self.parser.positionalArguments()

		#self.setWindowTitle(sys.argv[-1] if (len(sys.argv) and not __name__ == "__main__") else "tPlayer")
		self.setWindowIcon(Media.icon("default.ico", ""))
		self.setStyleSheet("Label{color:white;font-size: 16px;};")

	def checkFiles(self):
		if len(self.files):
			Media.addFile(self.files[0].replace("\\", "/"))

	def getInstance():

		if not Player.instance:
			Player.instance = Player()
		return Player.instance

	def start():

		print(Application.getInstance())

		player = Player.getInstance()
		player.show()
		player.checkFiles()


		sys.exit(app.exec())


Player.start()