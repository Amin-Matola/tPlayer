from PySide6.QtWidgets import (
	QToolBar, QSlider, QStatusBar, QWidget, QPushButton,
	QSizePolicy, QLabel, QFileDialog, QComboBox, QWidget
	)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from styles import theme
import os
from media import Media
from components.slider import Slider
from playlist import PlayList

class Menu:

	def __init__(self, app):
		self.app = app
		self.menu = app.menuBar()
		self.toolbar = QToolBar()
		self.progress = QToolBar()
		self.controls = QToolBar()
		self.adds = QToolBar()
		self.speeds = QComboBox()
		self.rate	= Slider(Qt.Horizontal, self.app)
		self.playlist = PlayList(app)

		self.init()

	def init(self):
		self.speeds.addItems(["1", "1.25", "1.30", "1.35", "1.40", "1.45", "1.50", "1.75", "2"])
		#self.rate.setTextVisible(False)

	def setMenus(self):
		self.file_menu 	= self.menu.addMenu("&File")
		self.help 		= self.menu.addMenu("&Help")
		self.passed 	= theme.label("0:00")
		self.max 		= theme.label("0:00")

	def setToolBar(self):
		self.app.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolbar)

	def setActions(self):
		self.open = QAction(
					Media.icon("play.png"), "&Open", 
					shortcut=QKeySequence.Open,
					triggered=lambda: Media.selectFile,
					parent=self.app)

		self.list = QAction("&Playlist")

		self.play = QAction(Media.icon("play.png"), "&Play", 
					shortcut="Ctrl+P",
					parent=self.app)
		self.prev = QAction(Media.icon("previous.png"), "&Previous", 
					shortcut="Ctr+R",
					parent=self.app)
		self.next = QAction(Media.icon("next.png"), "&Next", 
					shortcut="Ctrl+N",
					parent=self.app)
		self.speed = QPushButton(Media.icon("volume.png"), "")
		self.volume = QSlider(Qt.Horizontal, self.app)
		self.volume.setVisible(False)
		
		self.file_menu.addAction(self.open)
		self.file_menu.addAction(self.list)
		self.center(self.controls, [self.prev, self.play, self.next])
		self.progress.addWidget(self.passed)
		self.progress.addWidget(self.rate)
		self.progress.addWidget(self.max)
		
		self.controls.addWidget(self.speeds)
		self.controls.addWidget(self.speed)

		self.toolbar.setOrientation(Qt.Vertical)
		self.toolbar.addWidget(self.progress)
		self.toolbar.addWidget(self.adds)
		self.toolbar.addWidget(self.controls)

		theme.style(self.progress, "progress")
		theme.style(self.controls, "controls")
		theme.style(self.adds, "padding-right: 20px;")
		theme.style(self.speed, "margin-right: 10px;margin-left: 10px;")

	def getAction(self, name, icon, s, triggered = lambda: False, parent = None):
		return QAction(Media.icon(icon), name, 
					shortcut=s,
					triggered = triggered,
					parent=parent
				)

	def setCallbacks(self):
		self.open.triggered.connect(Media.selectFile)
		self.play.triggered.connect(lambda: Media.play(self.play))
		self.list.triggered.connect(self.playlist.createPlaylist)
		self.rate.valueChanged.connect(self.changeValue)
		self.next.triggered.connect(Media.next)
		self.prev.triggered.connect(Media.prev)
		self.speed.clicked.connect(self.setSpeed)
		self.volume.sliderMoved.connect(self.setVolume)
		self.speeds.currentIndexChanged.connect(self.changeSpeed)

	def setVolume(self):
		speed = self.volume.sliderPosition()

		Media.setVolume(speed)

	def changeSpeed(self):
		sp = float(self.speeds.currentText())
		Media.player.player.setPlaybackRate(sp)

	def setSpeed(self):
		if self.volume.isVisible():
			self.volume.setVisible(False)
		else:
			left = QWidget()
			left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			self.volume.setVisible(True)
			self.adds.addWidget(left)
			self.adds.addWidget(self.volume)
			self.volume.setMaximumWidth(100)
			self.volume.setMaximum(0)
			self.volume.setMaximum(100)

		

	def ten(self, i):
		i = int(i)
		item = str(i)
		if i < 10:
			item = f"0{item}"

		return item

	def getValue(self, millis):
		hours = round(( (millis/(1000*60*60))%24 ), 2)
		minutes = self.ten((millis/(1000*60)) % 60)
		secs = self.ten((millis/1000) % 60)
		text = f"{minutes}:{secs}"

		if hours >= 1:
			text = f"{self.ten(hours)}:{minutes}:{secs}"

		return text
		

	def changeValue(self, val):
		self.passed.setText(self.getValue(val))
		self.max.setText(self.getValue(self.rate.maximum() - val))


	def center(self, toolbar, actions = []):
		# spacer widget for left
		left = QWidget()
		right = QWidget()
		left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		toolbar.addWidget(left)

		for action in actions:
			toolbar.addAction(action)

		toolbar.addWidget(right)


	def config(app):
		menu = Menu(app)
		menu.setMenus()
		menu.setToolBar()
		menu.setActions()
		menu.setCallbacks()

		Media.config(app, menu.play, menu.rate, menu.playlist)

		return menu
