from PySide6.QtWidgets import (
	QToolBar, QProgressBar, QStatusBar, QWidget
	, QSizePolicy, QLabel, QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction, QKeySequence
from styles import theme
import os
from media import Media

class MenuController:

	def __init__(self, app):
		self.app = app
		self.menu = app.menuBar()
		self.toolbar = QToolBar()
		self.progress = QToolBar()
		self.controls = QToolBar()
		self.rate	= QProgressBar()

		self.init()

	def init(self):
		self.rate.setTextVisible(False)

	def setMenus(self):
		self.file_menu 	= self.menu.addMenu("&File")
		self.help 		= self.menu.addMenu("&Help")
		self.passed 	= theme.label("0:00")
		self.max 		= theme.label("0:00")

	def setToolBar(self):
		self.app.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolbar)

	def setActions(self):
		self.open = QAction(QIcon("icons/play.png"), "&Open", 
					shortcut=QKeySequence.Open,
					triggered=lambda: Media.selectFile,
					parent=self.app)

		self.play = QAction(QIcon("icons/play.png"), "&Play", 
					shortcut="Ctrl+P",
					parent=self.app)
		self.prev = QAction(QIcon("icons/previous.png"), "&Previous", 
					shortcut="Ctr+R",
					parent=self.app)
		self.next = QAction(QIcon("icons/next.png"), "&Next", 
					shortcut="Ctrl+N",
					parent=self.app)

		
		self.file_menu.addAction(self.open)
		self.center(self.controls, [self.prev, self.play, self.next])
		self.progress.addWidget(self.passed)
		self.progress.addWidget(self.rate)
		self.progress.addWidget(self.max)

		self.toolbar.setOrientation(Qt.Vertical)
		self.toolbar.addWidget(self.progress)
		self.toolbar.addWidget(self.controls)

		theme.style(self.progress, "progress")
		theme.style(self.controls, "controls")

	def setCallbacks(self):
		self.open.triggered.connect(Media.selectFile)
		self.play.triggered.connect(lambda: Media.play(self.play))
		self.rate.valueChanged.connect(self.changeValue)

	def getValue(self, v, h = 0):
		val = round((v/1000)/60, 2)
		text = "%.2f" % (val)

		if val > 60:
			h = int(val/60)
			return self.getValue(val - (h * 60), h)

		if(val < 10):
			text = "0%.2f" % (val)

		hour = str(h)
		if (h < 10):
			hour = f"0{hour}"

		if (h > 0):
			text = f"{hour}:{text}"


		return (text).replace(".", ":")

	def changeValue(self, val):
		self.passed.setText(self.getValue(val))
		self.max.setText(self.getValue(self.rate.maximum() - val))


	def center(self, toolbar, actions = []):
		# spacer widget for left
		left_spacer = QWidget()
		right_spacer = QWidget()
		left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		toolbar.addWidget(left_spacer)

		for action in actions:
			toolbar.addAction(action)

		toolbar.addWidget(right_spacer)


	def config(app):
		menu = MenuController(app)
		menu.setMenus()
		menu.setToolBar()
		menu.setActions()
		menu.setCallbacks()

		Media.config(app, menu.play, menu.rate)

		return menu



