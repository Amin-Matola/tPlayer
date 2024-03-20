from components.label import Label
from PySide6.QtWidgets import QLabel

styles = {
	"round": "border-radius: 10px",
	"progress": """
			margin-left:10px;margin-right:10px;
			height: 10px;
			""",
	"controls": """QToolButton{margin: 0 2px; padding: 2px 7.5px;}""",
	"label": "font-size: 15px;padding-bottom: 3px;",
	"cover": "background-image: url(%s) cover no-repeat; margin: 0 %dpx;",
}


class Style:

	def widget(w, style = ""):
		widget = w()

		if (len(styled)):
				widget.setStyleSheet(styles[style])

		return widget

	def style(self, item, name):
		if name in styles:
			item.setStyleSheet(styles[name])
		else:
			item.setStyleSheet(name)

		return item

	def label(self, name, style = "", media = None, main = False):
		label = QLabel(name)

		if main:
			label = Label(name, media)
		label.setStyleSheet(styles['label'] + style)

		return label

	def cover(self, item, cover, default = 30):

		self.style(item, styles["cover"] % (cover, default))



theme = Style()