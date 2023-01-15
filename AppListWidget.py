from __future__ import annotations
from PySide6.QtWidgets import  QListWidget, QListWidgetItem
from PySide6.QtGui import QKeyEvent, Qt
from typing import Callable, TYPE_CHECKING

# to prevent circular imports
if TYPE_CHECKING:
    from ListItem import ListItem


class AppListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentSelectedIndex = 0 

        self.setSpacing(20)
        self.setMinimumHeight(300)
        self.itemClicked.connect(None)

    def get_item_widget(self, index) -> ListItem:
        return self.itemWidget(self.item(index))

    def add_list_item(self, list_item: ListItem, clicked_callback: Callable):
        item = QListWidgetItem()
        item.setSelected(True)
        list_item.clicked.connect(clicked_callback)
        self.addItem(item)
        self.setItemWidget(item, list_item)

    def reset_selection(self):
        for i in range(self.count()):
            item = self.get_item_widget(i)
            item.set_selected(False)

    def set_selected_index(self, index):
        self.reset_selection()
        self.currentSelectedIndex = index
        list_item: ListItem = self.itemWidget(self.item(self.currentSelectedIndex))
        list_item.set_selected(True)

    def select_down(self):
        self.currentSelectedIndex -= 1
        if self.currentSelectedIndex < 0:
            self.currentSelectedIndex = 0
        self.reset_selection()
        list_item: ListItem = self.get_item_widget(self.currentSelectedIndex)
        list_item.set_selected(True)
        self.scrollToItem(self.item(self.currentSelectedIndex))

    def trigger_item_clicked(self, index):
        item = self.get_item_widget(index)
        item.clicked.emit(item)

    def select_up(self):
        self.currentSelectedIndex += 1
        if self.currentSelectedIndex >= self.count():
            self.currentSelectedIndex = self.count() - 1
        self.reset_selection()
        list_item: ListItem = self.get_item_widget(self.currentSelectedIndex)
        list_item.set_selected(True)
        self.scrollToItem(self.item(self.currentSelectedIndex))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # keys handle are reversed

        if event.key() == Qt.Key.Key_Return:
            self.trigger_item_clicked(self.currentSelectedIndex)

        if event.key() == Qt.Key.Key_Down:
            self.select_up()

        if event.key() == Qt.Key.Key_Up:
            self.select_down()
            

        # return super().keyPressEvent(event)

