from glob import glob
from os import path
import os
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QUrl
from media import Media

class PlayList:

	def __init__(self, app, folder = ""):
		self.playlist = []
		self.folder = folder.strip("/")
		self.app = app

		self.init()

	def init(self):

		if len(self.folder):
			self.createPlaylist()

	def config(app):
		playlist = PlayList(app)

		return playlist

	def createPlaylist(self):
		folder = QFileDialog.getExistingDirectory(
			self.app, 
			"Select Playlist Folder",
			Media.getMusicFolder(),
			QFileDialog.ShowDirsOnly
		)

		files = glob(f"{folder}/*.*")

		for file in files:
			if file.lower().endswith((".mp3", ".mp4")):
				f = path.join(folder, path.basename(file)).replace("\\", "/")
				self.playlist.append(f)

		if len(self.playlist):
			self.current = self.playlist[0]
			Media.addFile(self.current)

	def getNext(self, _increment = 1):
		index = -1

		if self.current in self.playlist:
			index = self.playlist.index(self.current)

		_next = index + _increment

		if _next >= len(self.playlist) or _next < 0:
			_next = 0

		self.current = self.playlist[_next]

		return self.current

	def getPrev(self):
		return self.getNext(-1)

	def isEmpty(self):
		return not len(self.playlist)


		
		

