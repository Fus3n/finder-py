from PySide6.QtWidgets import (
    QMenu,
    QLineEdit
)
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import Qt, QKeyEvent
from . import AppListWidget

INPUT_BOX_STYLE = """
background: #282A3A; 
font-size: 21px; 
border-radius: 5px;
color: #D8D8D8;
padding: 13px 13px;
"""

class SearchInput(QLineEdit):

    debounce_timeout = Signal()
    
    def __init__(self, list_view: AppListWidget ,dobounce_delay: float = -1, parent=None):
        super(SearchInput, self).__init__(parent)
        self.list_view = list_view

        # Setup stylesheet
        self.setStyleSheet(INPUT_BOX_STYLE)
        self.setPlaceholderText("Start typing...")
        self.setAlignment(Qt.AlignLeading)

        # Input debouncing
        self.timer = QTimer()
        self.timer.setInterval(dobounce_delay if dobounce_delay != -1 else 0)
        self.timer.timeout.connect(self.timer_timeout)
        self.textChanged.connect(self.input_changed)

    def input_changed(self):
        self.timer.stop()
        self.timer.start()

    def timer_timeout(self):
        """
        Debouncing is used to prevent unnecessary input noise/changes
        if we are going to execute a long running task after taking input.
        We don't want to execute it after every key press so if we 
        add a delay to wait after last key press, and reset it 
        after every key press we remove that extra presses.

        This function will execute after the delay has stopped so the logic
        that would go to input_changed can go in the debounc timeout signal or here
        """        
        self.debounce_timeout.emit()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("""
        QMenu {
            font-size: 14px; 
        }
        """)
        copy_action = menu.addAction("Copy")
        paste_action = menu.addAction("Paste")
        cut_action = menu.addAction("Cut")
        select_all_action = menu.addAction("Select All")

        copy_action.setShortcut("Ctrl+C")
        paste_action.setShortcut("Ctrl+P")
        cut_action.setShortcut("Ctrl+X")
        select_all_action.setShortcut("Ctrl+A")

        # Add more actions

        
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copy_action:
            self.copy()
        elif action == paste_action:
            self.paste()
        elif action == cut_action:
            self.cut()
        elif action == select_all_action:
            self.selectAll()
            pass

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Return:
            self.list_view.trigger_item_clicked(self.list_view.currentSelectedIndex)

        if event.key() == Qt.Key.Key_Down:
            self.list_view.select_up()

        if event.key() == Qt.Key.Key_Up:
            self.list_view.select_down()     

        
        return super().keyPressEvent(event)