from PySide6.QtWidgets import QSlider
from PySide6.QtGui import Qt
from media import Media

class Slider (QSlider):

	def __init__(self, orient, parent = None):
		super(Slider, self).__init__(orient, parent)

	def mousePressEvent(self, e):
		if e.button() == Qt.LeftButton:
			e.accept()
			x = e.pos().x()
			value = (self.maximum() - self.minimum()) * x / self.width() + self.minimum()
			self.setValue(value)

			Media.player.released()
		else:
			return super().mousePressEvent(self, e)


