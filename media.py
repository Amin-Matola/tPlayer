from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtGui import QIcon, QPixmap, QImage, QPalette, QColor
from PySide6.QtWidgets import QFileDialog
from libs import *
from PySide6.QtCore import Qt, QUrl
import os, time, sys
from os import path
import eyed3

#color = QPalette.setColor(QPalette.Text, QColor("white"))

class Media:

	player = None

	def __init__(self, app, playlist = None):
		self.app = app
		self.player = QMediaPlayer()
		self.played = False
		self.playButton = None
		self.playButton = None
		self.playlist = playlist
		self.screenshot = theme.label(
			"No media selected",
			"",
			Media,
			main = True
		)

	def setUp(self):

		self.video = QVideoWidget()
		self.audio = QAudioOutput()

		self.geom = self.app.screen().availableGeometry()

		
		self.video.setStyleSheet("margin: 0 10px")
		self.video.resize(self.geom.width(), 500)
		
		self.player.setVideoOutput(self.video)
		self.player.setAudioOutput(self.audio)
		self.app.setCentralWidget(self.screenshot)

		self.player.durationChanged.connect(self.setMax)
		self.player.positionChanged.connect(self.setPosition)
		
		theme.cover(self.screenshot, Media.cover("default.jpg"), 1)
		self.screenshot.setAlignment(Qt.AlignCenter)

	def setVolume(vol = 1):
		Media.player.audio.setVolume(vol)

	def setMax(self):
		val = self.player.duration()
		self.progress.setMinimum(0)
		self.progress.setMaximum(val)

	def notEmpty(self):
		return self.player.hasVideo() or self.player.hasAudio()

	def setPosition(self, position):
		val = position
		self.progress.setValue(val)

		if (val >= self.player.duration()):
			if self.playlist:
				Media.addFile(self.playlist.getNext())

	def released(self):
		
		pos = self.progress.sliderPosition()

		#print(pos, self.progress.value())
		
		if pos != self.player.position():
			self.player.setPosition(pos)
			time.sleep(.01)
		#self.progress.setValue(pos)


	def config(app, item = None, progress = None, pl = None):
		Media.player = Media(app, pl)
		Media.player.setUp()
		Media.player.setPlay(item, progress)

		return Media.player

	def setPlay(self, item, progress):
		self.playButton = item
		self.progress = progress
		self.progress.sliderMoved.connect(self.released)
		#self.progress.sliderPressed.connect(self.released)
		#self.progress.sliderReleased.connect(self.released)


	def getPlayer():
		return Media.player.player

	def addFile(item):
		media 	= Media.player
		player 	= Media.getPlayer()
		
		if not item:
			return

		if item.lower().endswith(".mp3"):
			file = eyed3.load(item)
			tag = file.tag
			images = tag.images
			if len(images):
				im = images[0]
				img = open(Media.absolute("cover.png"), "wb")
				img.write(im.image_data)
				img.close()
				#px = QPixmap(img.name)
				theme.cover(media.screenshot, Media.cover(img.name))
				media.screenshot.setText("")
			else:
				theme.cover(media.screenshot, Media.cover("default.jpg"),1)
				media.screenshot.setText(tag.title or path.basename(item))
		else:
			media.app.setCentralWidget(Media.player.video)

		# if player.isPlaying():
		# 	player.stop()

		#player.setSource(item)

		if item and player.isPlaying():
			player.stop()

			time.sleep(.01)
			Media.play(None, item)

		Media.play(None, item)

	def play(item = None, fl = None):

		player = Media.player.player

		if fl:
			player.setSource(QUrl(fl))

		# if not player.hasAudio() and not player.hasVideo():
		# 	return

		if not item:
			item = Media.player.playButton

		if item:
			if player.isPlaying():
				player.pause()
				item.setIcon(Media.icon("play.png"))
			else:
				item.setIcon(Media.icon("pause.png"))
				player.play()
		else:
			print("Item not available")

	def selectFile():
		file = QFileDialog.getOpenFileName(None, 
			"Open File", 
			Media.getMusicFolder(),
			"Files (*.mp4 *.mp3)")

		Media.addFile(file[0])

	def absolute(item, folder = ""):

		p = path.join(folder, item)

		if getattr( sys, 'frozen', False ):
			p = os.path.join(sys._MEIPASS, folder, item)

		return p

	def icon(icon, folder = "icons"):
		return QIcon(Media.absolute(icon, folder))

	def cover(icon):
		return Media.absolute(icon, "covers").replace("\\", "/")

	def next():
		player = Media.getPlayer()
		media 	= Media.player

		if not media.playlist or media.playlist.isEmpty():
			val = player.position() + (10 * 1000)
			player.setPosition(val)

		else:
			Media.addFile(media.playlist.getNext())

	def getMusicFolder(folder = "Music"):
		hp = path.expanduser("~")
		p = path.join(hp, folder)

		return p

	def prev():
		
		player = Media.getPlayer()
		media = Media.player;
		if not media.playlist or media.playlist.isEmpty():
			val = player.position() - (10 * 1000)

			if val < 0:
				val = 0
			player.setPosition(val)
		else:
			Media.addFile(media.playlist.getPrev())


