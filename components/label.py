from PySide6.QtWidgets import QLabel
from PySide6.QtGui import Qt

class Label (QLabel):
	def __init__(self, label = "", media = None):
		super(Label, self).__init__(label)
		self.media = media

	def mousePressEvent(self, e):
		if e.button() == Qt.MouseButton.LeftButton:
			if self.media:
				self.media.selectFile()
