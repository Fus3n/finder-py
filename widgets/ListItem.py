from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout
from PySide6.QtGui import QMouseEvent, QKeyEvent, Qt, QPixmap
from PySide6.QtCore import Signal

from .AppListWidget import AppListWidget


DEFAULT_STYLE_SHEET = """
    QWidget:hover {
        background-color: #353648;
    }
    QLabel {
        color: #D8D8D8;
        font-size: 15px;
        background-color: transparent;
        font-family: Roboto;
        margin-left: 10px;
    }
    QPushButton {
        background-color: #252631;
        width: 80px;
        height: 20px;
        color: #D8D8D8;
    }
"""


class ListItem(QFrame):
    
    clicked = Signal(type)

    def __init__(self, parent: AppListWidget, text: str, icon_pixmap: QPixmap, index: int):
        super().__init__(parent)
        self.list_view = parent
        self.text = text
        self.icon_pixmap = icon_pixmap
        self.index = index

        self.is_selected = False

        # Setup Layout for custom ListItem
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
        # height for each box
        self.setMinimumHeight(50)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(DEFAULT_STYLE_SHEET)

        icon = QLabel()
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_pixmap = self.icon_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(self.icon_pixmap)
        if len(self.text) > 50:
            text = self.text[:50] + '...'

        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(label)

    def select_item(self):
        """Deselect all other items and select this item"""
        # remove other selection/s
        self.list_view.reset_selection()
        # update selected on current item
        self.set_selected(True)
        # update selected on list view
        self.list_view.set_selected_index(self.index)

    def set_selected(self, value: bool):
        self.is_selected = value
        
        if value:
            self.setStyleSheet("QWidget { background-color: #404258; }" + DEFAULT_STYLE_SHEET)
        else:
            self.setStyleSheet(DEFAULT_STYLE_SHEET)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Enter:
            self.clicked.emit(self)
        return super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)

    